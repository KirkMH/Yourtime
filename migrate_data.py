import django
import os
from django.apps import apps
from django.db import connections, transaction

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YourTime.settings")
django.setup()

# Define database connections
sqlite_conn = connections['sqlite']
mysql_conn = connections['default']


def get_table_dependency_order():
    """
    Sorts tables to migrate parent tables first based on foreign key relationships.
    """
    models = apps.get_models()
    table_order = []
    processed = set()

    def add_table(model):
        if model in processed:
            return

        for field in model._meta.fields:
            if field.is_relation and field.related_model:
                add_table(field.related_model)

        table_order.append(model)
        processed.add(model)

    for model in models:
        add_table(model)

    return table_order


def migrate_data():
    models = get_table_dependency_order()

    # Disable foreign key checks in MySQL
    with mysql_conn.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

    for model in models:
        table_name = model._meta.db_table  # Get table name
        print(f"📤 Migrating: {table_name}")

        # Delete existing records before inserting new ones
        with mysql_conn.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name};")
            print(f"🗑️ Deleted all records from {table_name}")

        with sqlite_conn.cursor() as sqlite_cursor, mysql_conn.cursor() as mysql_cursor:
            # Fetch all data from SQLite
            sqlite_cursor.execute(f"SELECT * FROM {table_name}")
            rows = sqlite_cursor.fetchall()
            columns = [desc[0] for desc in sqlite_cursor.description]

            # Prepare MySQL INSERT statement
            placeholders = ", ".join(['%s'] * len(columns))
            insert_sql = f"INSERT INTO {table_name} ({', '.join(f'`{col}`' for col in columns)}) VALUES ({placeholders})"

            # for row in rows:
            #     try:
            #         # Print to see which record is being inserted
            #         # print(f"Inserting: {row}")
            #         # Insert one record at a time
            #         mysql_cursor.execute(insert_sql, row)
            #     except Exception as e:
            #         # Print error details for debugging
            #         print(f"Error with row {row}: {e}")
            #         print(mysql_cursor.mogrify(insert_sql, row))
            #         return

            # Insert into MySQL
            with transaction.atomic(using='default'):
                try:
                    mysql_cursor.executemany(insert_sql, rows)
                except Exception as e:
                    print(f"❌ Error inserting data into {table_name}: {e}")
                    continue

            print(f"✅ {len(rows)} records migrated from {table_name}")

    # Re-enable foreign key checks in MySQL
    with mysql_conn.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

    print("🎉 Data migration completed successfully!")


# Run the migration
if __name__ == "__main__":
    migrate_data()
