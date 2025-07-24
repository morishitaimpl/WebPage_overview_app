# WebPage_overview_app
Webページの要約アプリケーション - Claude AIを使用してWebページの内容を自動要約するStreamlitアプリ

## 概要

このアプリケーションは、指定されたWebページのURLから内容を取得し、Anthropic社のClaude AIモデルを使用して日本語で要約を生成するWebアプリケーションです。

## 機能

- WebページのURL入力による自動スクレイピング
- 複数のClaude AIモデルから選択可能（Claude 3.5 Sonnet、Claude 3.7 Sonnet、Claude Sonnet 4、Claude Opus 4）
- 温度パラメータの調整によるAI出力の制御
- リアルタイムストリーミング出力
- 要約結果と元のテキストの両方を表示

## ファイル構成

### agent.py
アプリケーションのエントリーポイントとなるメインファイル。シンプルで明確な構造になっています：

- **main()**: アプリケーションのメイン処理ループ
  - config.pyから各種機能をインポートして使用
  - URL入力の受け取り
  - URL妥当性の検証
  - Webページコンテンツの取得
  - AI要約の実行とストリーミング表示
  - 元のテキストの表示

**設計の特徴：**
- 関心の分離：UIロジックと設定・処理ロジックを分離
- config.pyモジュールを使用した機能の外部化
- 簡潔で読みやすいメイン処理フロー

### config.py
アプリケーションの設定と主要な処理機能を提供するモジュール：

- **AI_prompt**: Webページ要約用のプロンプトテンプレート
  - 日本語での要約指示
  - セクション単位での整理を指示
  - 箇条書きとまとまりを意識した形式

- **init_page()**: Streamlitページの初期設定
  - ページタイトルの設定
  - ヘッダーとサイドバーの初期化

- **select_model()**: AIモデルの選択とパラメータ設定
  - 温度パラメータのスライダー（0.0-1.0）
  - 4つのClaudeモデルから選択可能：
    - Claude 3.5 Sonnet (8,192トークン)
    - Claude 3.7 Sonnet (32,000トークン)
    - Claude Sonnet 4 (64,000トークン)
    - Claude Opus 4 (64,000トークン)

- **init_chain()**: LangChainを使用したAI処理チェーンの初期化
  - プロンプト、LLM、出力パーサーの連携

- **validate_url()**: 入力されたURLの妥当性検証
  - URLパースによるスキームとネットロケーションの確認

- **get_content()**: Webページからのコンテンツ取得
  - requestsライブラリによるHTTP通信
  - BeautifulSoupによるHTMLパース
  - main → article → bodyタグの優先順位でテキスト抽出
  - エラーハンドリングとユーザーフィードバック

**技術的な特徴：**
- モジュラー設計による保守性の向上
- 複数のClaudeモデルサポート
- エラーハンドリングの実装
- Streamlitセッション状態の活用

### requirements.txt
アプリケーションの依存関係を定義するファイル：

- **tiktoken**: OpenAIのトークナイザーライブラリ（トークン数計算用）
- **streamlit**: Webアプリケーションフレームワーク（UI構築）
- **langchain-core**: LangChainのコア機能（AI処理チェーン）
- **langchain-anthropic**: Anthropic Claude AI用のLangChainインテグレーション
- **requests**: HTTP通信ライブラリ（Webページ取得）

**注意事項：**
- BeautifulSoup4の依存関係が明記されていないため、別途インストールが必要
- ANTHROPIC_API_KEYの環境変数設定が必要

## セットアップ

1. 依存関係のインストール：
```bash
pip install -r requirements.txt
pip install beautifulsoup4  # 追加で必要
```

2. 環境変数の設定：
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

3. アプリケーションの実行：
```bash
streamlit run agent.py
```

## 使用方法

1. ブラウザでアプリケーションにアクセス
2. サイドバーでAIモデルと温度パラメータを選択
3. URLフィールドに要約したいWebページのURLを入力
4. 自動的に要約が生成され、元のテキストと共に表示される

## 技術スタック

- **フロントエンド**: Streamlit
- **AI処理**: LangChain + Anthropic Claude
- **Webスクレイピング**: requests + BeautifulSoup
- **言語**: Python 3.x

## アーキテクチャの特徴

### 改善されたコード構造
リポジトリの修正により、以下の改善が実現されています：

1. **関心の分離**: 
   - `agent.py`: アプリケーションのエントリーポイントとメインフロー
   - `config.py`: 設定、AI処理、ユーティリティ機能

2. **モジュラー設計**:
   - 機能ごとに適切に分離された関数
   - 再利用可能なコンポーネント
   - 保守性の向上

3. **明確な依存関係**:
   - `agent.py`が`config.py`をインポートする単方向の依存
   - 循環依存の回避

### 今後の拡張可能性
- 新しいAIモデルの追加が容易
- 異なるWebスクレイピング戦略の実装
- 追加のUI機能の組み込み
- テスト機能の追加
