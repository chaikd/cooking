from langgraph.checkpoint.postgres import PostgresSaver

class CheckpointManager:
    saver = None
    def __init__(self):
        super().__init__()
    def initialize(self, database):
        saver = PostgresSaver(database.pool)
        saver.setup()
        self.saver = saver

checkpoint_manager = CheckpointManager()