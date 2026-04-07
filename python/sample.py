from pyavd import get_device_config

# 1. デバイスの設定データ（Structured Config）を定義
structured_config = {
    "hostname": "leaf1",
    "ethernet_interfaces": [
        {
            "name": "Ethernet1",
            "description": "P2P_LINK_TO_SPINE1",
            "shutdown": False,
            "ip_address": "192.168.1.1/31",
        }
    ],
    "management_interfaces": [
        {"name": "Management1", "ip_address": "10.0.0.11/24", "gateway": "10.0.0.1"}
    ],
}

# 2. コンフィグの生成
# get_device_config は EOS の設定テキストを返します
try:
    eos_config = get_device_config(structured_config)

    print("--- Generated EOS Config ---")
    print(eos_config)
except Exception as e:
    print(f"Error generating config: {e}")
