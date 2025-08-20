from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from prompt import prompt


@register(
    "spaghetti_concrete",
    "OpenAI",
    "一本正经胡说八道生成器",
    "1.0.0",
    "https://github.com/example/spaghetti_concrete",
)
class SpaghettiConcrete(Star):
    """基于“意大利面混凝土理论”的荒谬因果链生成器"""

    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("sc", alias={"spaghetti"})
    async def sc(self, event: AstrMessageEvent, keyword: str = ""):
        """生成荒谬的跨领域伪学术论证"""
        base_prompt = prompt
        if keyword.strip():
            final_prompt = (
                f"{base_prompt}\n请以“{keyword}”作为因果链起点，生成一段论证。"
            )
        else:
            final_prompt = (
                f"{base_prompt}\n随机选择一个日常事物作为因果链起点，生成一段论证。"
            )

        try:
            yield event.request_llm(prompt=final_prompt)
        except Exception as exc:  # pragma: no cover - best effort logging
            logger.error(f"SpaghettiConcrete error: {exc}")
            yield event.plain_result("生成失败，请稍后再试。")
