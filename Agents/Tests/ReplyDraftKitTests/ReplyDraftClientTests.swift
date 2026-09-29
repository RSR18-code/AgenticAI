import Foundation
import XCTest
@testable import ReplyDraftKit

final class ReplyDraftClientTests: XCTestCase {
    func testAppendsChatCompletionsToBaseEndpoint() throws {
        let url = try ReplyDraftClient.completionsURL(from: XCTUnwrap(URL(string: "https://api.example.com/v1/")))
        XCTAssertEqual(url.absoluteString, "https://api.example.com/v1/chat/completions")
    }

    func testDoesNotDuplicateChatCompletionsPath() throws {
        let url = try ReplyDraftClient.completionsURL(
            from: XCTUnwrap(URL(string: "https://api.example.com/v1/chat/completions"))
        )
        XCTAssertEqual(url.absoluteString, "https://api.example.com/v1/chat/completions")
    }

    func testDoesNotDuplicateRootChatCompletionsPath() throws {
        let url = try ReplyDraftClient.completionsURL(
            from: XCTUnwrap(URL(string: "https://api.example.com/chat/completions"))
        )
        XCTAssertEqual(url.absoluteString, "https://api.example.com/chat/completions")
    }

    func testRejectsInsecureRemoteEndpoint() throws {
        XCTAssertThrowsError(
            try ReplyDraftClient.completionsURL(from: XCTUnwrap(URL(string: "http://api.example.com/v1")))
        ) { error in
            XCTAssertEqual(error as? ReplyDraftError, .invalidEndpoint)
        }
    }

    func testAllowsLocalDevelopmentEndpoint() throws {
        let url = try ReplyDraftClient.completionsURL(
            from: XCTUnwrap(URL(string: "http://localhost:8080/v1"))
        )
        XCTAssertEqual(url.absoluteString, "http://localhost:8080/v1/chat/completions")
    }

    func testRequiresAPIKeyBeforeMakingRequest() async throws {
        let client = ReplyDraftClient()
        let configuration = DraftConfiguration(
            endpoint: try XCTUnwrap(URL(string: "https://api.example.com/v1")),
            model: "test-model",
            apiKey: " \n"
        )

        do {
            _ = try await client.generateDraft(for: "Hello", tone: .natural, configuration: configuration)
            XCTFail("Expected an empty API key to be rejected.")
        } catch let error as ReplyDraftError {
            XCTAssertEqual(error, .missingAPIKey)
        }
    }
}
