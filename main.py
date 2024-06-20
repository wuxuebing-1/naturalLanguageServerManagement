# main.py

import openai
import paramiko
import config
import requests

# 设置 OpenAI API 密钥
openai.api_key = config.OPENAI_API_KEY


def get_command_from_gpt(prompt, use_proxy=False):
    formatted_prompt = f"Provide only the command for: {prompt}"
    if use_proxy:
        response = requests.post(
            config.PROXY_API_URL,
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': formatted_prompt}],
                'temperature': 0.7
            },
            headers={'Authorization': f'Bearer {config.OPENAI_API_KEY}'}
        )
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Error decoding JSON response: {response.text}")
            return ""
        return response_data['choices'][0]['message']['content'].strip()
    else:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=formatted_prompt,
            max_tokens=50
        )
        return response.choices[0].text.strip()


def execute_command_on_server(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config.SERVER_IP, username=config.SERVER_USERNAME, password=config.SERVER_PASSWORD)

    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()
    ssh.close()
    return output + error


def format_output(output):
    lines = output.split('\n')
    formatted_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(formatted_lines)


def main():
    while True:
        user_input = input("请输入要执行的服务器命令（输入'退出'结束程序）：")
        if user_input.lower() == '退出':
            break

        # 根据配置选择使用 OpenAI 官方接口或代理接口
        command = get_command_from_gpt(user_input, use_proxy=config.USE_PROXY)
        print(f"解析的命令: {command}")

        if command:
            result = execute_command_on_server(command)
            formatted_result = format_output(result)
            print(f"服务器返回的结果:\n{formatted_result}")


if __name__ == "__main__":
    main()