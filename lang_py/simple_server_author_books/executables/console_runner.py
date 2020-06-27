from data.dummy_data_wrapper import get_schema


def run():
    schema = get_schema()
    while(True):
        my_query = input("Enter a GraphQL query ([Enter] to confirm, [^C] to exit):")
        result = schema.execute(my_query)
        print(result.data)
