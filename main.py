def main():
    import os

    from taskmaster import TaskMaster
    from utils import download, find_last_comic_num

    # ---------- CONSTANTS ----------
    downloads_per_thread = 15
    target_repository_folder = os.path.join(os.environ['USERPROFILE'], 'Desktop\\comics_folder')
    # -------------------------------

    if not os.path.isdir(target_repository_folder):
        os.makedirs(target_repository_folder)

    stats = {'downloads': 0}
    task_master = TaskMaster(
        target_function=download,
        dest=target_repository_folder,
        stats=stats
    )

    last = find_last_comic_num()
    for start in range(1, last, downloads_per_thread):
        end = last + 1 if start + downloads_per_thread > last else start + downloads_per_thread
        task_master.create_download_task(range_start=start, range_end=end)
    task_master.initialize_tasks()
    task_master.wait_until_completion()

    print('Done.')
    print(f'Successful downloads: {stats["downloads"]}.')


if __name__ == '__main__':
    main()
