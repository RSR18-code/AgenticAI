import ReplyDraftKit
import SwiftUI
import UIKit

struct DraftView: View {
    @AppStorage("apiEndpoint") private var apiEndpoint = "https://api.openai.com/v1"
    @AppStorage("modelName") private var modelName = "gpt-4o-mini"
    @State private var message = ""
    @State private var draft = ""
    @State private var tone: ReplyTone = .natural
    @State private var isGenerating = false
    @State private var errorMessage: String?
    @State private var isShowingSettings = false
    @State private var copied = false

    var body: some View {
        NavigationStack {
            Form {
                Section("Message") {
                    TextEditor(text: $message)
                        .frame(minHeight: 150)
                        .accessibilityLabel("Message to reply to")
                    Picker("Tone", selection: $tone) {
                        ForEach(ReplyTone.allCases, id: \.self) { tone in
                            Text(tone.rawValue.capitalized).tag(tone)
                        }
                    }
                }

                Section {
                    Button(action: generateDraft) {
                        HStack {
                            Spacer()
                            if isGenerating {
                                ProgressView()
                                    .padding(.trailing, 6)
                                Text("Drafting…")
                            } else {
                                Label("Draft a reply", systemImage: "sparkles")
                            }
                            Spacer()
                        }
                    }
                    .disabled(isGenerating || message.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                }

                if !draft.isEmpty {
                    Section("Reply draft") {
                        TextEditor(text: $draft)
                            .frame(minHeight: 130)
                            .accessibilityLabel("Editable reply draft")
                        Button {
                            UIPasteboard.general.string = draft
                            copied = true
                        } label: {
                            Label(copied ? "Copied" : "Copy reply", systemImage: copied ? "checkmark" : "doc.on.doc")
                        }
                    }
                }

                Section {
                    Text("Your message is sent to the configured AI endpoint only when you tap Draft. The app never sends replies.")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Reply Assistant")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        isShowingSettings = true
                    } label: {
                        Image(systemName: "gearshape")
                    }
                    .accessibilityLabel("Settings")
                }
            }
            .sheet(isPresented: $isShowingSettings) {
                SettingsView()
            }
            .alert("Couldn’t create a draft", isPresented: errorIsPresented) {
                Button("OK", role: .cancel) {}
            } message: {
                Text(errorMessage ?? "An unknown error occurred.")
            }
        }
    }

    private var errorIsPresented: Binding<Bool> {
        Binding(
            get: { errorMessage != nil },
            set: { if !$0 { errorMessage = nil } }
        )
    }

    private func generateDraft() {
        guard let endpoint = URL(string: apiEndpoint) else {
            errorMessage = ReplyDraftError.invalidEndpoint.localizedDescription
            return
        }

        isGenerating = true
        draft = ""
        copied = false

        Task {
            defer { isGenerating = false }
            do {
                let apiKey = try APIKeyStore.read() ?? ""
                let configuration = DraftConfiguration(
                    endpoint: endpoint,
                    model: modelName.trimmingCharacters(in: .whitespacesAndNewlines),
                    apiKey: apiKey
                )
                draft = try await ReplyDraftClient().generateDraft(
                    for: message,
                    tone: tone,
                    configuration: configuration
                )
            } catch {
                errorMessage = error.localizedDescription
            }
        }
    }
}
