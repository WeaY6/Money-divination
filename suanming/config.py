from openai import OpenAI
from main import cast_hexagram, parse_manual_input, display_hexagram_result, get_hexagram_name

# DeepSeek API配置
API_KEY = "sk-"  # 需要替换为实际的API密钥

# 话术模板
def generate_prompt(hexagram_name, changing_lines, changed_hexagram_name, question_type):
    """
    生成发送给DeepSeek AI的话术模板
    
    参数:
    hexagram_name: 主卦名称
    changing_lines: 变爻位置列表
    changed_hexagram_name: 变卦名称
    question_type: 用户咨询的问题类型
    
    返回:
    格式化的话术字符串
    """
    # 处理变爻信息
    changing_lines_text = ""
    if changing_lines:
        changing_positions = [str(i+1) for i in changing_lines]
        changing_lines_text = f"其中第{', '.join(changing_positions)}爻为变爻，变为{changed_hexagram_name}。"
    else:
        changing_lines_text = "无变爻。"
    
    # 生成完整话术
    prompt = f"我通过金钱起卦法，得到{hexagram_name}，{changing_lines_text}我占问的是关于{question_type}的困惑。请从易学专业的角度答疑解惑，分析卦象含义，解读吉凶，并给出相应的建议。"
    
    return prompt

# 调用DeepSeek API获取解读
def get_ai_interpretation(prompt):
    """
    调用DeepSeek API获取易经解读
    
    参数:
    prompt: 发送给AI的话术
    
    返回:
    AI的解读结果
    """
    # 初始化OpenAI客户端
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.deepseek.com/v1"  # DeepSeek API的基础URL
    )
    
    try:
        # 提示用户正在等待API响应
        print("正在请求DeepSeek AI解读，请稍候...")
        
        # 使用OpenAI客户端调用API
        response = client.chat.completions.create(
            model="deepseek-chat",  # 使用DeepSeek Chat模型
            messages=[
                {"role": "system", "content": "你是一位精通易经的专业易学老师，擅长解读卦象，分析吉凶，给出专业的指导和建议。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        # 获取生成的内容
        content = response.choices[0].message.content
        
        # 添加免责声明
        disclaimer = """

免责声明：本算法仅用于易学课题研究与学习目的，所提供的解读结果仅供参考，不构成任何形式的专业建议。用户不应将本解读作为人生重大决策的唯一依据，也不应用于商业用途、医疗诊断、法律咨询或其他专业领域。本系统不对因使用解读结果而导致的任何直接或间接损失承担责任。请用户理性看待解读结果，并在做出重要决策时咨询相关专业人士的意见。本系统不支持任何形式的迷信活动，不应被用于违反法律法规或公序良俗的目的。如有任何问题欢迎联系作者WY 谢谢。
"""
        
        # 返回添加了免责声明的内容
        return content + disclaimer
    except Exception as e:
        return f"发生错误: {str(e)}"

# 整合起卦和AI解读功能
def divination_with_ai_interpretation(mode, input_str=None, question_type=""):
    """
    整合起卦和AI解读功能
    
    参数:
    mode: 起卦模式，1为自动起卦，2为手动输入
    input_str: 手动输入的卦象字符串，仅在mode=2时使用
    question_type: 用户咨询的问题类型，如事业发展/感情抉择/健康等
    
    返回:
    AI的解读结果
    """
    # 获取卦象结果
    hexagram_code = None
    changing_lines = None
    
    if mode == 1:  # 自动起卦
        print("自动起卦中...")  
        hexagram_code, changing_lines = cast_hexagram(print_result=True)
    elif mode == 2:  # 手动输入
        hexagram_code, changing_lines = parse_manual_input(input_str)
    else:
        return "无效的起卦模式"
    
    if hexagram_code is None:
        return "起卦失败"
    
    # 计算变卦
    changed_hexagram_code = hexagram_code
    if changing_lines:
        changed_lines = list(hexagram_code)
        for i in changing_lines:
            changed_lines[i] = '1' if hexagram_code[i] == '0' else '0'
        changed_hexagram_code = ''.join(changed_lines)
    
    # 获取卦名
    hexagram_name = get_hexagram_name(hexagram_code)
    changed_hexagram_name = get_hexagram_name(changed_hexagram_code)
    
    # 生成话术
    prompt = generate_prompt(hexagram_name, changing_lines, changed_hexagram_name, question_type)
    
    # 获取AI解读
    interpretation = get_ai_interpretation(prompt)
    
    return interpretation

# 示例使用方法
def example_usage():
    print("易经起卦与AI解读系统")
    print("1. 自动起卦 - 模拟抛硬币")
    print("2. 手动输入卦象")
    
    mode = input("请选择模式 (1/2): ")
    question_type = input("请输入您想咨询的问题类型(如事业发展/感情抉择/健康等): ")
    
    if mode == '1':
        result = divination_with_ai_interpretation(1, question_type=question_type)
    elif mode == '2':
        input_str = input("请输入卦象 (例如: +++AB-): ")
        result = divination_with_ai_interpretation(2, input_str, question_type)
    else:
        print("无效的选择")
        return
    
    print("\n====== deepseek AI解读结果 ======")
    print(result)

if __name__ == "__main__":
    example_usage()