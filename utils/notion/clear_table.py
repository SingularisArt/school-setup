def clear_table(notion, table_id):
    records = notion.databases.query(table_id)

    for record in records["results"]:
        notion.blocks.delete(record["id"])
