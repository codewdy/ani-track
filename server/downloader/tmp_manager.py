import uuid
import os

class TmpManager:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.dir = None
        self.allocated_files = []

    def allocate_file(self, name):
        path = os.path.join(self.dir, name)
        self.allocated_files.append(path)
        return path

    def start(self):
        while True:
            name = str(uuid.uuid4())
            path = os.path.join(self.root_dir, name)
            try:
                os.makedirs(path)
            except FileExistsError:
                continue
            self.dir = path
            return

    def close(self):
        try:
            os.rmdir(self.dir)
        except OSError:
            for file in self.allocated_files:
                try:
                    os.remove(file)
                except OSError:
                    pass

    async def __aenter__(self):
        self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()

if __name__ == "__main__":
    import asyncio
    async def test():
        async with TmpManager("/tmp/test") as manager:
            print(manager.allocate_file("test.txt"))
    asyncio.run(test())
