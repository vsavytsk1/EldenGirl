# ios/ — codex only (ships last, possibly never)

Its own build. Shares a threat model with `docs/` and `android/` and **nothing else**.

## Why this tier is the smallest, on purpose

`docs/THE_APP_v1_3.md` records an honest platform blocker: `CFBundleDisplayName` is static, so
iOS cannot switch its name and icon at runtime the way the Android cover does. **So iOS may be a
reading app only** — the codex, presented plainly — until that blocker moves. The encrypted
record tier does **not** come to iOS on a guess.

There is also `v1.5` III·6: **Keychain items survive app deletion.** If the record tier is ever
built here, panic wipe cannot rely on the user deleting the app — key material is deleted
explicitly, and stored `WhenUnlockedThisDeviceOnly` with `kSecAttrSynchronizable = false`, or it
rides iCloud Keychain into an account he controls (Adversary B). G8 enforces this.

## What is here now

| file | what it does | gate |
|---|---|---|
| `App/SnapshotObscuring.swift` | covers the UI when the app backgrounds, so the app-switcher snapshot reveals nothing | G5 (iOS form) |
| `App/Info.plist` | no `NS*UsageDescription` keys, so no permission is ever requested | G1 (iOS form) |
| `App/App.entitlements` | keychain access only — nothing else | G1, G8 |

iOS has no `FLAG_SECURE`. The equivalent is to install an obscuring view on
`sceneWillResignActive` and remove it on `sceneDidBecomeActive`, then verify by backgrounding and
reading the snapshot from the sandbox — because the API contract is not the behaviour.

## What is deliberately NOT here

- Any permission usage string (`NS*UsageDescription`) — G1's iOS form fails on any.
- Any Swift Package, CocoaPod or Carthage dependency — G2 fails if `Package.resolved`,
  `Podfile.lock` or `Cartfile.resolved` exists at all.
- Any biometric / `LocalAuthentication` call — compellable, banned (G8).
- The record tier, until the name blocker moves and an advocate review says so.

## Building

Open in Xcode, or generate a project. No third-party package manager is permitted, so there is
no dependency-resolution step by design.

**Green means nothing broke. It does not mean it works.**
