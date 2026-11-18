from pathlib import Path
RULE_VERSION = "2026.11.18.2"
TITLE = '卫星条带覆盖与云区筛选'
SHORT = 'swath-cover'
MODULES = ['条带接收', '坐标契约', '云区剔除', '覆盖并集', '缺口定位', '采购候选', '交付核验']
HEADERS = ['scene', 'alias', 'west', 'east', 'cloud_w', 'cloud_e', 'quality', 'price', 'captured', 'version']
SAMPLE = Path(__file__).resolve().parent.parent / "sample_data" / "operations.csv"
LIMIT = 10000
