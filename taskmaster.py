from threading import Thread


class TaskMaster:

    def __init__(self, target_function, dest, stats):
        self.dest = dest
        self.function = target_function
        self.stats = stats
        self.tasks: list[Thread] = []

    def create_download_task(self, range_start: int, range_end: int):
        new_task = Thread(target=self.function, kwargs={
            'range_start': range_start,
            'range_end': range_end,
            'dest': self.dest,
            'stats': self.stats
        })
        self.tasks.append(new_task)
        print(f'{len(self.tasks)} task(s) created')

    def initialize_tasks(self):
        for task in self.tasks:
            task.start()
        print('All tasks initialized.')

    def wait_until_completion(self):
        for task in self.tasks:
            task.join()
