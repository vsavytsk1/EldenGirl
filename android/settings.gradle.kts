// The android tier is its own build. It shares a threat model with web/ and ios/
// and NOTHING else — no code, no storage, no release cycle (v1.5 Part 0).
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    // FAIL_ON_PROJECT_REPOS keeps every dependency source declared in one place,
    // so the G2 allowlist has a single graph to check against.
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "cover"
include(":app")
