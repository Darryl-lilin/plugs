import psutil


def close_application(application_name):
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == f'{application_name}.exe':
                proc.kill()
                print(f'{application_name} 进程已关闭。')
                return
        print(f'未找到 {application_name} 进程。')

    except Exception as e:
        print(f'关闭 {application_name} 进程时出错：{e}')


# 调用函数关闭应用进程
close_application('close')  # 替换为要关闭的应用程序名称
