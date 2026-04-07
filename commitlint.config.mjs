// Conventional Commits configuration, consumed by the CI workflow
// (.github/workflows/commitlint.yml). Local enforcement is handled by
// .githooks/commit-msg so contributors don't need Node installed.
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'header-max-length': [2, 'always', 100],
    'subject-case': [
      2,
      'never',
      ['sentence-case', 'start-case', 'pascal-case', 'upper-case'],
    ],
  },
};
