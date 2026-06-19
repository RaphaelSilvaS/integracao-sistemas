class Constants {
  // =====================================================
  // CONFIGURAÇÃO FIREBASE — ALTERE AQUI
  // Siga o README.md para obter esses valores gratuitamente
  // =====================================================

  // Web API Key — Firebase Console > Configurações do Projeto > Web API Key
  static const FIREBASE_API_KEY = 'AIzaSyCKNk9uRu0Xwk9oYdjpioHyXUOkv1NRrNY';

  // URL do Realtime Database — Firebase Console > Realtime Database > URL
  static const FIREBASE_DB_URL = 'https://projeto-integrador-303c5-default-rtdb.firebaseio.com';

  // =====================================================
  // URLs da API — não altere abaixo desta linha
  // =====================================================
  static const USER_FAVORITES_URL = '$FIREBASE_DB_URL/userFavorites';
  static const PRODUCT_BASE_URL = '$FIREBASE_DB_URL/products';
  static const ORDER_BASE_URL = '$FIREBASE_DB_URL/orders';
}
