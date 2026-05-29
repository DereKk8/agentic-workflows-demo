from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Sistema Agéntico de Mesa de Ayuda Académica"
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/agentic_helpdesk"
    modo_agente: str = "mock"
    proveedor_llm: str = "groq"
    groq_api_key: str | None = None
    openrouter_api_key: str | None = None
    gemini_api_key: str | None = None
    model_groq: str = "llama-3.1-8b-instant"
    model_openrouter: str = "openai/gpt-4o-mini"
    model_gemini: str = "gemini-1.5-flash"
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()

