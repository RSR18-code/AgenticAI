import Foundation

public enum ReplyTone: String, CaseIterable, Sendable {
    case natural
    case warm
    case concise
    case professional

    public var instruction: String {
        switch self {
        case .natural: "Write a natural, conversational reply."
        case .warm: "Write a warm and friendly reply."
        case .concise: "Write a concise reply."
        case .professional: "Write a polite, professional reply."
        }
    }
}

public struct DraftConfiguration: Sendable {
    public let endpoint: URL
    public let model: String
    public let apiKey: String

    public init(endpoint: URL, model: String, apiKey: String) {
        self.endpoint = endpoint
        self.model = model
        self.apiKey = apiKey
    }
}

public enum ReplyDraftError: Error, LocalizedError, Sendable, Equatable {
    case missingAPIKey
    case missingModel
    case invalidEndpoint
    case invalidResponse
    case requestFailed(statusCode: Int)

    public var errorDescription: String? {
        switch self {
        case .missingAPIKey:
            "Add your API key in Settings before generating a draft."
        case .missingModel:
            "Enter a model name in Settings before generating a draft."
        case .invalidEndpoint:
            "Enter a valid HTTPS API endpoint. HTTP is allowed only for localhost."
        case .invalidResponse:
            "The API returned a response that could not be used. Check the endpoint and model."
        case .requestFailed(let statusCode):
            "The API request failed (HTTP \(statusCode)). Check your API key, model, and endpoint."
        }
    }
}

public struct ReplyDraftClient: Sendable {
    private let session: URLSession

    public init(session: URLSession = .shared) {
        self.session = session
    }

    public func generateDraft(
        for message: String,
        tone: ReplyTone,
        configuration: DraftConfiguration
    ) async throws -> String {
        let apiKey = configuration.apiKey.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !apiKey.isEmpty else {
            throw ReplyDraftError.missingAPIKey
        }
        let model = configuration.model.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !model.isEmpty else {
            throw ReplyDraftError.missingModel
        }

        let url = try Self.completionsURL(from: configuration.endpoint)
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.httpBody = try JSONEncoder().encode(ChatCompletionRequest(
            model: model,
            messages: [
                .init(role: "system", content: """
                Draft a reply to the message the user shares. \(tone.instruction) \
                Return only the reply text. Do not claim to be the user or send the message.
                """),
                .init(role: "user", content: message)
            ]
        ))

        let (data, response) = try await session.data(for: request)
        guard let response = response as? HTTPURLResponse else {
            throw ReplyDraftError.invalidResponse
        }
        guard (200..<300).contains(response.statusCode) else {
            throw ReplyDraftError.requestFailed(statusCode: response.statusCode)
        }

        let decoded = try JSONDecoder().decode(ChatCompletionResponse.self, from: data)
        guard let draft = decoded.choices.first?.message.content
            .trimmingCharacters(in: .whitespacesAndNewlines),
              !draft.isEmpty else {
            throw ReplyDraftError.invalidResponse
        }
        return draft
    }

    static func completionsURL(from endpoint: URL) throws -> URL {
        guard var components = URLComponents(url: endpoint, resolvingAgainstBaseURL: false),
              let scheme = components.scheme?.lowercased(),
              let host = components.host?.lowercased(),
              components.user == nil,
              components.password == nil,
              components.query == nil,
              components.fragment == nil,
              scheme == "https" || (scheme == "http" && ["localhost", "127.0.0.1", "::1"].contains(host))
        else {
            throw ReplyDraftError.invalidEndpoint
        }

        let path = components.path.trimmingCharacters(in: CharacterSet(charactersIn: "/"))
        if path == "chat/completions" || path.hasSuffix("/chat/completions") {
            components.path = "/" + path
        } else {
            components.path = "/" + [path, "chat/completions"].filter { !$0.isEmpty }.joined(separator: "/")
        }
        guard let url = components.url else {
            throw ReplyDraftError.invalidEndpoint
        }
        return url
    }
}

private struct ChatCompletionRequest: Encodable {
    struct Message: Encodable {
        let role: String
        let content: String
    }

    let model: String
    let messages: [Message]
}

private struct ChatCompletionResponse: Decodable {
    struct Choice: Decodable {
        struct Message: Decodable {
            let content: String
        }

        let message: Message
    }

    let choices: [Choice]
}
