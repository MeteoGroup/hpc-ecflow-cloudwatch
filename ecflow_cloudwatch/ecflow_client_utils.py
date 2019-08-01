import os
import ecflow


class GetEcflowStats(object):

    def fetch_ecflow_stats(self):
        # Create the client. This will read the default environment variables
        ecflow_host = os.getenv('ECF_HOST', "localhost")
        ecflow_port = os.getenv('ECF_PORT', "3143")
        ci = ecflow.Client(ecflow_host, ecflow_port)

        # Get the node tree suite definition as stored in the server
        # The definition is retrieved and stored on the variable 'ci'
        ci.sync_local()

        # access the definition retrieved from the server
        server_defs = ci.get_defs()

        if server_defs == None :
            print "The server has no definition"
            exit(1)
        return server_defs

