import SwiftUI

struct SettingsView: View {
    @AppStorage("apiEndpoint") private var apiEndpoint = "https://api.openai.com/v1"
    @AppStorage("modelName") private var modelName = "gpt-4o-mini"
    @Environment(\.dismiss) private var dismiss
    @State private var apiKey = ""
    @State private var errorMessage: String?

    var body: some View {
        NavigationStack {
            Form {
                Section("AI endpoint") {
                    TextField("https://api.openai.com/v1", text: $apiEndpoint)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                        .keyboardType(.URL)
                    TextField("Model", text: $modelName)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                    SecureField("API key", text: $apiKey)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                } footer: {
                    Text("Use an OpenAI-compatible Chat Completions endpoint. Your API key is stored in this device’s Keychain.")
                }

                Section {
                    Button("Save settings", action: save)
                }
            }
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button("Close") { dismiss() }
                }
            }
            .task {
                do {
                    apiKey = try APIKeyStore.read() ?? ""
                } catch {
                    errorMessage = error.localizedDescription
                }
            }
            .alert("Settings error", isPresented: errorIsPresented) {
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

    private func save() {
        do {
            try APIKeyStore.save(apiKey)
            dismiss()
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}
