from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
 
class Server:
    def __init__(self, contact_points=['127.0.0.1'], port=9042, username='cassandra', password='cassandra'):
        auth_provider = PlainTextAuthProvider(username=username, password=password)
        self.cluster = Cluster(contact_points, port=port, auth_provider=auth_provider)
        self.session = self.cluster.connect()
        self.keyspace = "project3"
        self.table = "data"
 
        try:
            # Create keyspace and table
            self.session.execute(
                "CREATE KEYSPACE IF NOT EXISTS " + self.keyspace +
                " WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};"
            )
            self.session.set_keyspace(self.keyspace)
            self.session.execute(
                f"CREATE TABLE IF NOT EXISTS {self.table} (key text PRIMARY KEY, value text);"
            )
        except Exception as e:
            print("Failed to setup database:", e)
            raise
 
    def add_data(self, key, value):
        try:
            insert_query = f"INSERT INTO {self.table} (key, value) VALUES (%s, %s);"
            self.session.execute(insert_query, (key, value))
        except Exception as e:
            print("Error adding data:", e)
            raise
 
    def get_data(self, key):
        try:
            select_query = f"SELECT value FROM {self.table} WHERE key = %s;"
            result = self.session.execute(select_query, (key,))
            return result.one()[0] if result.one() else None
        except Exception as e:
            print("Error retrieving data:", e)
            raise
 
    def close(self):
        self.session.shutdown()
        self.cluster.shutdown()
 
