# Reply Assistant

A native iPhone starter app for drafting replies to messages you paste in. It does not connect to WhatsApp, read chats, or send replies.

## Open and run

1. Open `iOS/ReplyDraftAssistant.xcodeproj` in Xcode.
2. Select the ReplyDraftAssistant app target and set your Apple development team for signing.
3. Run on an iPhone simulator or device running iOS 17 or later.
4. In the app, open Settings and enter an OpenAI-compatible API endpoint, model name, and API key.

The default endpoint is `https://api.openai.com/v1` and the default model is `gpt-4o-mini`. The API key is stored in the device Keychain. The message is sent to the configured endpoint only when you tap **Draft a reply**. Review and edit the generated draft, then copy it back into WhatsApp yourself.

This first version uses copy/paste. A WhatsApp share-sheet extension is not included yet.

## Reply-drafting library

The shared request and response handling lives in `Sources/ReplyDraftKit`. The package tests cover endpoint validation and API-key checks; run them with `swift test` in a full Xcode installation.
