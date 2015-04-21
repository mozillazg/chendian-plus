#开发

## 安装依赖

    # 推荐创建依赖环境
    # virtualenv venv
    # source venv/bin/active

    pip install -r requirements_dev.txt

## 运行开发服务器

    cp chendian/chendian/settings_dev.py.sample chendian/chendian/settings_dev.py
    make server
    # 或 python chendian/manager_dev.py runserver
