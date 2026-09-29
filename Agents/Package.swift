// swift-tools-version: 6.0

import PackageDescription

let package = Package(
    name: "ReplyDraftKit",
    platforms: [
        .iOS(.v16),
        .macOS(.v12),
    ],
    products: [
        .library(
            name: "ReplyDraftKit",
            targets: ["ReplyDraftKit"]
        ),
    ],
    targets: [
        .target(
            name: "ReplyDraftKit"
        ),
        .testTarget(
            name: "ReplyDraftKitTests",
            dependencies: ["ReplyDraftKit"]
        ),
    ],
    swiftLanguageModes: [.v6]
)
