# Claude Code × Codex 連携セットアップ

## 1. 準備（各自のPCで1回だけ）

```bash
# Claude Code
npm install -g @anthropic-ai/claude-code

# Codex CLI
npm install -g @openai/codex
codex login
```

## 2. Claude Code から Codex を使う

このリポジトリの `.mcp.json` に Codex が登録済みです。
リポジトリで `claude` を起動すると、プロジェクトの MCP サーバーを使ってよいか確認されるので承認してください。

```bash
claude mcp list   # codex が表示されればOK
```

使えるスラッシュコマンド:

| コマンド | 内容 |
| --- | --- |
| `/codex-review [観点]` | 現在の diff を Codex にレビューさせ、妥当な指摘だけ反映 |
| `/codex-ask <質問>` | Codex にセカンドオピニオンを聞き、Claude の意見と比較 |

## 3. Codex から Claude Code を使う（任意）

`~/.codex/config.toml` に次を追加します。

```toml
[mcp_servers.claude]
command = "claude"
args = ["mcp", "serve"]
```

## 4. ルールファイル

- `AGENTS.md` … 共通ルール（Codex が読む）
- `CLAUDE.md` … `@AGENTS.md` で共通ルールを読み込み、Claude Code 固有の設定を追記

ルールを変えるときは基本的に `AGENTS.md` だけ編集してください。

## トラブルシューティング

- `codex: command not found` → Codex CLI のインストールと PATH を確認
- MCP がつながらない → `codex mcp-server` を単体で実行してエラーを確認
- オプション名が違う → バージョンで変わることがあるので `codex --help` / `claude mcp --help` で確認
