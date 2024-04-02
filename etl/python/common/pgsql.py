import csv
from io import StringIO


def copy_expert(table, conn, keys, data_iter) -> int:
    """
    A function that copies data from a CSV-like data iterator to a database table using the copy_expert method.

    Args:
        table: The table object representing the destination table in the database.
        conn: The database connection object.
        keys: The list of column names to copy data into.
        data_iter: An iterator containing the data rows to be copied.

    Returns:
        int: The number of rows copied into the table.
    """
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        columns = ", ".join(f'"{k}"' for k in keys)
        table_name = f"{table.schema}.{table.name}" if table.schema else table.name

        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        sql = f"COPY {table_name} ({columns}) FROM STDIN WITH CSV"
        cur.copy_expert(sql=sql, file=s_buf)
        return cur.rowcount


def copy_expert_onconflict_skip(
    table, conn, keys, data_iter, return_ids: bool = False, pk: str | None = None
) -> int | list:
    """
    Copy data from data_iter into the specified table, handling conflicts according to the specified keys.
    Optionally return the IDs of the affected rows.

    Args:
        table: The table to copy data into.
        conn: The connection to the database.
        keys: The keys to use for conflict resolution.
        data_iter: An iterable providing the data to be copied.
        return_ids: Whether to return the IDs of affected rows (default is False).
        pk: The primary key of the table (only required if return_ids is True).

    Returns:
        If return_ids is True and pk is not None, a list of IDs of the affected rows;
        otherwise, the number of affected rows.
    """
    if return_ids is True and pk is None:
        raise ValueError("Can't return ids if pk is None")

    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        columns = ", ".join(f'"{k}"' for k in keys)
        table_name = f"{table.schema}.{table.name}" if table.schema else table.name

        # If ignored conflicting rows is important: create staging table
        tmp_table_name = table_name + "_tmp"
        cur.execute(f"CREATE TEMP TABLE {tmp_table_name} (LIKE {table_name})")

        # Prepare data to be copied
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        # Copy into table
        sql = f"COPY {tmp_table_name} ({columns}) FROM STDIN WITH CSV"
        cur.copy_expert(sql=sql, file=s_buf)

        # If ignored conflicting rows is important: insert into main table from temp and delete
        if return_ids:
            cur.execute(
                f"INSERT INTO {table_name} SELECT * FROM {tmp_table_name} ON CONFLICT DO NOTHING RETURNING {pk}"  # noqa: S608
            )
            result = [tup[0] for tup in cur.fetchall()]
        else:
            cur.execute(f"INSERT INTO {table_name} SELECT * FROM {tmp_table_name} ON CONFLICT DO NOTHING")  # noqa: S608
            result = cur.rowcount

        cur.execute(f"DROP TABLE {tmp_table_name}")

        return result
