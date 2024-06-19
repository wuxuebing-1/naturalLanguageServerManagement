# main.py

import openai
import paramiko
import config

# 设置 OpenAI API 密钥
openai.api_key = config.OPENAI_API_KEY


def get_command_from_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()


def execute_command_on_server(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config.SERVER_IP, username=config.SERVER_USERNAME, password=config.SERVER_PASSWORD)

    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    ssh.close()
    return output


def main():
    while True:
        user_input = input("请输入要执行的服务器命令（输入'退出'结束程序）：")
        if user_input.lower() == '退出':
            break

        command = get_command_from_gpt(user_input)
        print(f"GPT 解析的命令: {command}")

        result = execute_command_on_server(command)
        print(f"服务器返回的结果: {result}")


if __name__ == "__main__":
    main()