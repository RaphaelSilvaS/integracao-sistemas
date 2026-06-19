class AuthException implements Exception {
  static const Map<String, String> errors = {
    'EMAIL_EXISTS': 'E-mail ja existente.',
    'OPERATION_NOT_ALLOWED': 'Operacao nao é permitida.',
    'TOO_MANY_ATTEMPTS_TRY_LATER': ' Acesso bloqueado temporariamente. Tente mais tarde.',
    'EMAIL_NOT_FOUND': 'E-mail nao encontrado.',
    'INVALID_PASSWORD': 'Senha informada nao confere.',
    'USER_DISABLED': 'A conta do usuario foi desabilitada.',
    'INVALID_LOGIN_CREDENTIALS': 'Dados informados nao coincidem com cadastro.',
  };

  final String key;

  AuthException(this.key);

  @override
  String toString() {
    return errors[key] ?? 'Ocorreu um erro no processo de autenticacao';
  }
}
