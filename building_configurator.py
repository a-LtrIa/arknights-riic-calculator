"""
明日方舟基建配置工具 - Streamlit Web界面
用于配置房间、等级、进驻干员
"""

import streamlit as st
import json
from gold_bar_operators import 获取制造站干员, 制造站干员注册表


# 房间配置
ROOMS = {
    "制造站": {"数量": 3, "等级范围": (1, 5), "描述": "生产赤金、作战记录、源石"},
    "贸易站": {"数量": 3, "等级范围": (1, 5), "描述": "贸易加工"},
    "发电站": {"数量": 4, "等级范围": (1, 5), "描述": "提供电力"},
    "宿舍": {"数量": 4, "等级范围": (1, 5), "描述": "恢复干员心情"},
    "控制中枢": {"数量": 1, "等级范围": (1, 5), "描述": "提供特殊加成"},
    "会客室": {"数量": 1, "等级范围": (1, 5), "描述": "线索搜集"},
    "加工站": {"数量": 1, "等级范围": (1, 5), "描述": "加工技能材料"},
    "训练室": {"数量": 2, "等级范围": (1, 4), "描述": "干员精英化和技能升级"},
    "办公室": {"数量": 1, "等级范围": (1, 5), "描述": "办公任务"},
}

# 获取所有可用干员
def 获取所有干员列表():
    """获取所有可配置的干员名称列表"""
    return sorted(制造站干员注册表.keys())


def 创建默认配置():
    """创建默认配置"""
    配置 = {}
    for 房间名, 房间信息 in ROOMS.items():
        房间列表 = []
        for i in range(1, 房间信息["数量"] + 1):
            房间名_with_idx = f"{房间名}{i}" if 房间信息["数量"] > 1 else 房间名
            房间列表.append({
                "房间名": 房间名_with_idx,
                "等级": 1,
                "进驻干员": []
            })
        配置[房间名] = 房间列表
    return 配置


def 主函数():
    st.set_page_config(
        page_title="明日方舟基建配置器",
        page_icon="🏗️",
        layout="wide"
    )

    st.title("🏗️ 明日方舟基建配置器")
    st.markdown("配置房间、等级和进驻干员")

    # 初始化会话状态
    if "配置" not in st.session_state:
        st.session_state.配置 = 创建默认配置()
    if "结果字典" not in st.session_state:
        st.session_state.结果字典 = None

    # 侧边栏：操作按钮
    with st.sidebar:
        st.header("操作")
        if st.button("🔄 重置配置"):
            st.session_state.配置 = 创建默认配置()
            st.rerun()

        if st.button("💾 生成结果字典"):
            结果字典 = {}
            for 房间类型, 房间列表 in st.session_state.配置.items():
                for 房间 in 房间列表:
                    房间名 = 房间["房间名"]
                    干员列表 = 房间["进驻干员"]
                    if 干员列表:  # 只包含有干员的房间
                        结果字典[房间名] = 干员列表
            st.session_state.结果字典 = 结果字典

        if st.button("📋 复制到剪贴板"):
            if st.session_state.结果字典:
                st.code(json.dumps(st.session_state.结果字典, ensure_ascii=False, indent=2), language="json")
                st.info("请手动复制上面的JSON代码")

    # 主界面：房间配置
    所有干员列表 = 获取所有干员列表()

    tabs = st.tabs(list(ROOMS.keys()))

    for idx, (房间名, 房间信息) in enumerate(ROOMS.items()):
        with tabs[idx]:
            st.subheader(f"{房间名} (共{房间信息['数量']}间)")

            # 为每个房间创建配置项
            for i in range(房间信息["数量"]):
                房间配置 = st.session_state.配置[房间名][i]
                房间名_with_idx = 房间配置["房间名"]

                with st.expander(f"📦 {房间名_with_idx}", expanded=True):
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        # 等级选择
                        等级 = st.selectbox(
                            "等级",
                            options=list(range(房间信息["等级范围"][0], 房间信息["等级范围"][1] + 1)),
                            index=房间配置["等级"] - 房间信息["等级范围"][0],
                            key=f"等级_{房间名_with_idx}"
                        )
                        st.session_state.配置[房间名][i]["等级"] = 等级

                    with col2:
                        # 干员选择（多选）
                        selected_operators = st.multiselect(
                            "进驻干员 (最多3人)",
                            options=所有干员列表,
                            default=房间配置["进驻干员"],
                            max_selections=3,
                            key=f"干员_{房间名_with_idx}"
                        )
                        st.session_state.配置[房间名][i]["进驻干员"] = selected_operators

                    # 显示当前加成
                    if selected_operators:
                        st.markdown("**当前加成预览:**")
                        for 干员名 in selected_operators:
                            干员 = 获取制造站干员(干员名)
                            if 干员:
                                加成 = 干员.计算加成()
                                st.text(f"  - {加成}")

    # 底部：结果显示
    st.markdown("---")
    st.subheader("📊 配置结果")

    col1, col2 = st.columns([2, 1])

    with col1:
        if st.session_state.结果字典:
            st.json(st.session_state.结果字典)
        else:
            st.info("点击左侧「生成结果字典」按钮生成结果")

    with col2:
        if st.session_state.结果字典:
            st.metric("配置房间数", len(st.session_state.结果字典))
            总干员数 = sum(len(v) for v in st.session_state.结果字典.values())
            st.metric("进驻干员总数", 总干员数)


if __name__ == "__main__":
    主函数()
