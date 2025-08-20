from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import AstrBotConfig, logger
from .prompt import prompt


@register(
    "spaghetti_concrete",
    "KONpiGG",
    "一本正经胡说八道生成器",
    "1.0.0",
    "https://github.com/KONpiGG/spaghetti_concrete",
)
class SpaghettiConcrete(Star):
    """基于“意大利面混凝土理论”的荒谬因果链生成器"""

    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.provider_id = config.get("provider_id", "")

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

        provider = (
            self.context.get_provider_by_id(self.provider_id)
            if self.provider_id
            else self.context.get_using_provider()
        )

        if not provider:
            yield event.plain_result("未找到可用的 LLM 提供商，请检查配置。")
            return

        try:
            resp = await provider.text_chat(
                prompt=final_prompt,
                session_id=None,
                contexts=[],
                image_urls=[],
                func_tool=None,
                system_prompt="",
            )
            if resp.role == "assistant":
                yield event.plain_result(resp.completion_text)
            else:
                yield event.plain_result("生成失败，请稍后再试。")
        except Exception as exc:  # pragma: no cover - best effort logging
            logger.error(f"SpaghettiConcrete error: {exc}")
            yield event.plain_result("生成失败，请稍后再试。")
