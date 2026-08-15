#!/usr/bin/env python3
"""从结构化户外照片简报生成日式扁平插画编辑提示词。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCENE_DETAILS: dict[str, str] = {
    "高山/山谷": "远景使用层叠山脊、灰褐岩面与少量雪线，以大色块代替碎石和岩壁纹理",
    "峡谷观景台": "保留栏杆的横竖关系和远处峡谷层次，删除牌面小字、锈蚀和杂乱细节",
    "荒漠公路/入口": "使用浅褐沙地、灰蓝天空与简洁道路引导线交代开阔环境，不保留路牌或门楼小字",
    "雪地营地": "用白色、浅蓝和炭灰块面表现积雪和树干，帐篷保留为清晰的大色块，避免逐根树枝",
    "林间瀑布": "用深绿团簇、灰岩大块和两三条蓝白流线表现林地与瀑布，避免密集叶片和水花纹理",
    "营地/徒步步道": "用土黄步道、灌木团块与远山色块建立前中后景，保留与主体有关的露营装备",
}


def require_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"字段 {key!r} 必须是非空字符串。")
    return value.strip()


def require_string_list(data: dict[str, Any], key: str, minimum: int = 1) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or len(value) < minimum:
        raise ValueError(f"字段 {key!r} 必须是至少包含 {minimum} 项的字符串数组。")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"字段 {key!r} 只能包含非空字符串。")
    return [item.strip() for item in value]


def join_items(items: list[str]) -> str:
    return "、".join(items)


def build_prompt(data: dict[str, Any]) -> str:
    subject = require_string(data, "subject")
    composition = require_string(data, "composition")
    outfit_colors = require_string_list(data, "outfit_colors")
    anchors = require_string_list(data, "anchors", minimum=3)
    if len(anchors) > 6:
        raise ValueError("字段 'anchors' 最多保留 6 项，避免提示词失焦。")
    scene = require_string(data, "scene")
    mood = require_string(data, "mood")
    aspect_ratio = require_string(data, "aspect_ratio")
    preserve = require_string_list(data, "preserve")
    exclude = require_string_list(data, "exclude")
    text_policy = require_string(data, "text_policy")

    scene_detail = SCENE_DETAILS.get(
        scene,
        "将背景归纳为前、中、远三层的大色块，只保留能说明户外场景类型的少量元素",
    )

    if text_policy == "none":
        text_clause = "不要出现可读文字、数字、品牌标志、水印、签名或二维码"
    elif text_policy == "short_confirmed":
        text_content = require_string(data, "text_content")
        text_location = require_string(data, "text_location")
        text_clause = (
            f"仅在{text_location}渲染用户确认的短文本“{text_content}”；"
            "使用圆润、粗厚、略不规则但清晰可读的萌化手写印刷体，保留舒适边距；"
            "不要添加其他文字、品牌标志、水印、签名或二维码，且需要人工逐字核对文字准确性"
        )
    else:
        raise ValueError("字段 'text_policy' 仅支持 'none' 或 'short_confirmed'。")

    prompt = f"""编辑所提供的照片：仅将视觉表现转换为平和、温和的日式平面素材插画，不改变照片内容事实。
严格风格锁定：不是日漫，不是二次元，不是半写实。人物使用大而圆的头部、紧凑圆润的身体和极简图形化五官；只要嘴部未被遮挡，必须画一条小而友好的上扬短弧嘴；使用偏深棕的圆角粗线、5–8 个低至中饱和哑光色块，每个物体至多一层极浅阴影。背景必须是安静的大色块并留有干净空隙。
主体为{subject}。{composition}。保留{join_items(preserve)}；尤其保留以下视觉锚点：{join_items(anchors)}。服装与装备主色为{join_items(outfit_colors)}。
衣物和装备只保留外形、主色、位置和少量必要边界线。背景为{scene}：{scene_detail}。使用低至中饱和的暖色平面配色，前中后景清晰，主体边缘最易读，整体氛围{mood}。{text_clause}。
不要改变人物数量、姿势、头部遮挡关系、服装主色或关键装备；不要添加照片中没有的人、动物、车辆、帐篷、旗帜或地标；不要日漫或漫画渲染、写实脸部、皮肤建模、牙齿、睫毛、锐利黑线、赛璐璐阴影、密集线稿、细小扣具、真实材质、照片纹理、岩石纹理、单片树叶、复杂渐变、HDR、戏剧光影、3D、油画、赛博风、荧光色；不要畸形手指、额外手臂、漂浮背包或错误的装备握持。避免：{join_items(exclude)}。输出{aspect_ratio}，完整保留主体。"""
    return prompt


def main() -> int:
    parser = argparse.ArgumentParser(description="生成户外照片转日式扁平插画的中文编辑提示词。")
    parser.add_argument("--brief", type=Path, required=True, help="UTF-8 JSON 简报文件路径。")
    parser.add_argument("--output", type=Path, help="输出 Markdown 文件路径；省略时打印到标准输出。")
    args = parser.parse_args()

    try:
        raw = args.brief.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("简报根节点必须是 JSON 对象。")
        prompt = build_prompt(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2

    output = f"# 户外照片转日式扁平插画提示词\n\n{prompt}\n"
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8")
        except OSError as exc:
            print(f"错误：无法写入输出文件：{exc}", file=sys.stderr)
            return 2
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
