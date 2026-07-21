from langgraph.checkpoint.postgres import PostgresSaver

from database.postgres.postgres import database

class CheckpointManager:
    saver = None
    def __init__(self):
        super().__init__()
    def initialize(self):
        saver = PostgresSaver(database.poll)
        saver.setup()
        self.saver = saver

checkpoint_manager = CheckpointManager()