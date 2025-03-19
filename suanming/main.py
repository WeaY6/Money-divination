import random

# 八卦名称和符号
# 乾(天)、坤(地)、震(雷)、艮(山)、坎(水)、离(火)、巽(风)、兑(泽)
# 每个卦由三爻组成，从下到上排列
TRIGRAMS = {
    '111': {'name': '乾', 'symbol': '☰', 'nature': '天'},
    '000': {'name': '坤', 'symbol': '☷', 'nature': '地'},
    '100': {'name': '震', 'symbol': '☳', 'nature': '雷'},
    '001': {'name': '艮', 'symbol': '☶', 'nature': '山'},
    '010': {'name': '坎', 'symbol': '☵', 'nature': '水'},
    '101': {'name': '离', 'symbol': '☲', 'nature': '火'},
    '110': {'name': '巽', 'symbol': '☴', 'nature': '风'},
    '011': {'name': '兑', 'symbol': '☱', 'nature': '泽'}
}

# 六十四卦名称
HEXAGRAMS = {
    '111111': '乾为天', '000000': '坤为地', '010001': '水雷屯', '100010': '山水蒙',
    '010111': '水天需', '111010': '天水讼', '000010': '地水师', '010000': '水地比',
    '110111': '风天小畜', '111011': '天泽履', '000111': '地天泰', '111000': '天地否',
    '111101': '天火同人', '101111': '火天大有', '000100': '地山谦', '001000': '雷地豫',
    '011001': '泽雷随', '100110': '山风蛊', '000011': '地泽临', '110000': '风地观',
    '101001': '火雷噬嗑', '100101': '山火贲', '100000': '山地剥', '000001': '地雷复',
    '111001': '天雷无妄', '100111': '山天大畜', '100001': '山雷颐', '011110': '泽风大过',
    '010010': '坎为水', '101101': '离为火', '001110': '山泽损', '011100': '泽山咸',
    '111100': '天山遁', '001111': '雷天大壮', '101000': '火地晋', '000101': '地火明夷',
    '101011': '火泽睽', '110101': '风火家人', '001010': '水山蹇', '010100': '雷水解',
    '110001': '风雷益', '100011': '雷风恒', '000110': '地风升', '011000': '风地观',
    '011010': '泽水困', '010110': '水风井', '011101': '泽火革', '101110': '火风鼎',
    '001001': '震为雷', '100100': '艮为山', '001011': '风山渐', '110100': '雷泽归妹',
    '101100': '火山旅', '001101': '风火丰', '010101': '水火既济', '101010': '火水未济'
}

# 爻辞
LINE_TEXTS = {
    '9': '九', # 阳爻变
    '7': '七', # 阴爻变
    '6': '六', # 阴爻
    '8': '八'  # 阳爻
}

def toss_coins():
    """
    模拟抛三枚硬币
    1表示正面，2表示背面
    返回一个包含三个硬币结果的列表
    """
    return [random.randint(1, 2) for _ in range(3)]

def analyze_toss(coins):
    """
    分析抛硬币的结果
    返回爻的类型和是否变爻
    """
    # 计算正面(1)的数量
    heads = coins.count(1)
    
    # 根据规则判断爻的类型和是否变爻
    if heads == 3:  # 三个正面：阴爻变阳
        return '0', True  # 阴爻，变
    elif heads == 2:  # 两正一反：阳爻
        return '1', False  # 阳爻，不变
    elif heads == 1:  # 一正两反：阴爻
        return '0', False  # 阴爻，不变
    else:  # 三个背面：阳爻变阴
        return '1', True  # 阳爻，变

def get_line_symbol(line_type, changing):
    """
    获取爻的符号表示
    """
    if line_type == '1':  # 阳爻
        return '9' if changing else '8'
    else:  # 阴爻
        return '7' if changing else '6'

def get_hexagram_name(hexagram_code):
    """
    根据六爻代码获取卦名
    """
    return HEXAGRAMS.get(hexagram_code, '未知卦')

def get_trigram_info(trigram_code):
    """
    获取三爻卦的信息
    """
    return TRIGRAMS.get(trigram_code, {'name': '未知', 'symbol': '?', 'nature': '未知'})

def cast_hexagram(print_result=True):
    """
    完整的起卦过程
    
    参数:
    print_result: 是否打印结果，默认为True
    
    返回:
    hexagram_code: 卦象代码
    changing_lines: 变爻位置列表
    """
    lines = []
    changing_lines = []
    
    # 抛六次硬币
    for i in range(6):
        coins = toss_coins()
        line_type, changing = analyze_toss(coins)
        
        lines.append(line_type)
        if changing:
            changing_lines.append(i)
        
        if print_result:
            coin_result = ''.join(['正' if c == 1 else '反' for c in coins])
            line_symbol = get_line_symbol(line_type, changing)
            print(f"第{i+1}爻: 硬币结果 {coin_result} -> {LINE_TEXTS[line_symbol]}")
    
    hexagram_code = ''.join(lines)
    
    # 如果有变爻，计算变卦
    changed_hexagram_code = hexagram_code
    if changing_lines:
        changed_lines = list(hexagram_code)
        for i in changing_lines:
            changed_lines[i] = '1' if hexagram_code[i] == '0' else '0'
        changed_hexagram_code = ''.join(changed_lines)
    
    # 获取主卦和变卦的名称
    hexagram_name = get_hexagram_name(hexagram_code)
    changed_hexagram_name = get_hexagram_name(changed_hexagram_code)
    
    if print_result:
        lower_trigram_code = hexagram_code[:3]
        upper_trigram_code = hexagram_code[3:]
        lower_trigram = get_trigram_info(lower_trigram_code)
        upper_trigram = get_trigram_info(upper_trigram_code)
        
        print("\n====== 起卦结果 ======")
        print(f"主卦: {hexagram_name} ({upper_trigram['name']}{lower_trigram['name']})")
        print(f"上卦: {upper_trigram['name']}({upper_trigram['nature']}) {upper_trigram['symbol']}")
        print(f"下卦: {lower_trigram['name']}({lower_trigram['nature']}) {lower_trigram['symbol']}")
        
        # 如果有变爻，打印变卦信息
        if changing_lines:
            changed_lower_trigram_code = changed_hexagram_code[:3]
            changed_upper_trigram_code = changed_hexagram_code[3:]
            changed_lower_trigram = get_trigram_info(changed_lower_trigram_code)
            changed_upper_trigram = get_trigram_info(changed_upper_trigram_code)
            
            print(f"\n变卦: {changed_hexagram_name} ({changed_upper_trigram['name']}{changed_lower_trigram['name']})")
            print(f"上卦: {changed_upper_trigram['name']}({changed_upper_trigram['nature']}) {changed_upper_trigram['symbol']}")
            print(f"下卦: {changed_lower_trigram['name']}({changed_lower_trigram['nature']}) {changed_lower_trigram['symbol']}")
            
            print("\n变爻位置:")
            for i in changing_lines:
                print(f"第{i+1}爻")
    
    return hexagram_code, changing_lines

def parse_manual_input(input_str):
    """
    解析用户手动输入的卦象
    格式: 使用+表示阳爻，-表示阴爻，A表示阴爻变阳，B表示阳爻变阴
    例如: +++AB- 表示三个阳爻，一个阴爻变阳，一个阳爻变阴，一个阴爻
    """
    if len(input_str) != 6:
        print("错误: 输入必须是6个字符，分别代表6爻")
        return None, None
    
    lines = []
    changing_lines = []
    
    for i, char in enumerate(input_str):
        if char == '+':
            lines.append('1')  # 阳爻
        elif char == '-':
            lines.append('0')  # 阴爻
        elif char == 'A':
            lines.append('0')  # 阴爻变阳
            changing_lines.append(i)
        elif char == 'B':
            lines.append('1')  # 阳爻变阴
            changing_lines.append(i)
        else:
            print(f"错误: 无效的字符 '{char}'，请使用+、-、A或B")
            return None, None
    
    return ''.join(lines), changing_lines

def display_hexagram_result(hexagram_code, changing_lines):
    """
    显示卦象结果
    """
    # 如果有变爻，计算变卦
    changed_hexagram_code = hexagram_code
    if changing_lines:
        changed_lines = list(hexagram_code)
        for i in changing_lines:
            changed_lines[i] = '1' if hexagram_code[i] == '0' else '0'
        changed_hexagram_code = ''.join(changed_lines)
    
    # 获取主卦和变卦的名称
    hexagram_name = get_hexagram_name(hexagram_code)
    changed_hexagram_name = get_hexagram_name(changed_hexagram_code)
    
    lower_trigram_code = hexagram_code[:3]
    upper_trigram_code = hexagram_code[3:]
    lower_trigram = get_trigram_info(lower_trigram_code)
    upper_trigram = get_trigram_info(upper_trigram_code)
    
    print("\n====== 起卦结果 ======")
    print(f"主卦: {hexagram_name} ({upper_trigram['name']}{lower_trigram['name']})")
    print(f"上卦: {upper_trigram['name']}({upper_trigram['nature']}) {upper_trigram['symbol']}")
    print(f"下卦: {lower_trigram['name']}({lower_trigram['nature']}) {lower_trigram['symbol']}")
    
    # 如果有变爻，打印变卦信息
    if changing_lines:
        changed_lower_trigram_code = changed_hexagram_code[:3]
        changed_upper_trigram_code = changed_hexagram_code[3:]
        changed_lower_trigram = get_trigram_info(changed_lower_trigram_code)
        changed_upper_trigram = get_trigram_info(changed_upper_trigram_code)
        
        print(f"\n变卦: {changed_hexagram_name} ({changed_upper_trigram['name']}{changed_lower_trigram['name']})")
        print(f"上卦: {changed_upper_trigram['name']}({changed_upper_trigram['nature']}) {changed_upper_trigram['symbol']}")
        print(f"下卦: {changed_lower_trigram['name']}({changed_lower_trigram['nature']}) {changed_lower_trigram['symbol']}")
        
        print("\n变爻位置:")
        for i in changing_lines:
            print(f"第{i+1}爻")

def main():
    print("易经起卦模拟器")
    print("1. 自动起卦 - 模拟抛硬币")
    print("2. 手动输入卦象")
    print("3. 起卦并获取AI解读")
    print("\n自动起卦说明: 使用1代表硬币正面，2代表硬币背面")
    print("规则: 两正一反为阳卦，两反一正为阴卦")
    print("      三正为阴卦变阳卦，三反为阳卦变阴卦")
    print("\n手动输入说明: 使用+表示阳爻，-表示阴爻，A表示阴爻变阳，B表示阳爻变阴")
    print("例如: +++AB- 表示三个阳爻，一个阴爻变阳，一个阳爻变阴，一个阴爻\n")
    
    while True:
        choice = input("请选择模式 (1/2/3): ")
        
        if choice == '1':
            print("\n自动起卦模式")
            input("按回车键开始起卦...")
            cast_hexagram()
        elif choice == '2':
            print("\n手动输入模式")
            input_str = input("请输入卦象 (例如: +++AB-): ")
            hexagram_code, changing_lines = parse_manual_input(input_str)
            if hexagram_code is not None:
                display_hexagram_result(hexagram_code, changing_lines)
        elif choice == '3':
            try:
                # 尝试导入config模块中的功能
                from config import example_usage
                example_usage()
            except ImportError:
                print("错误: 无法导入config模块，请确保config.py文件存在且配置正确")
            except Exception as e:
                print(f"发生错误: {str(e)}")
        else:
            print("无效的选择，请输入1、2或3")
            continue
        
        continue_choice = input("\n是否继续? (y/n): ")
        if continue_choice.lower() != 'y':
            break

if __name__ == "__main__":
    
    main()