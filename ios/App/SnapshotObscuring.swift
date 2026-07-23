import UIKit

/// iOS has no FLAG_SECURE. The nearest equivalent is to obscure the UI while the
/// app is backgrounded, so the app-switcher snapshot iOS captures reveals nothing
/// (G5, iOS form -> S7). The obscuring view goes up on `sceneWillResignActive` —
/// BEFORE the snapshot is taken — and comes down on `sceneDidBecomeActive`.
///
/// ⚠️ The API contract is not the behaviour. This must be verified by backgrounding
///    the app and reading the captured snapshot from the sandbox in a test, not by
///    trusting that the callback fired.
final class SnapshotObscuring {

    private var shield: UIView?

    /// Call from `sceneWillResignActive`.
    func cover(_ window: UIWindow?) {
        guard let window, shield == nil else { return }
        let view = UIView(frame: window.bounds)
        view.backgroundColor = UIColor(red: 0.043, green: 0.043, blue: 0.059, alpha: 1)
        view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        window.addSubview(view)
        shield = view
    }

    /// Call from `sceneDidBecomeActive`.
    func reveal() {
        shield?.removeFromSuperview()
        shield = nil
    }
}
