import 'package:virtual_store/models/auth.dart';
import 'package:virtual_store/screens/auth_screen.dart';
import 'package:virtual_store/screens/products_overview_screen.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class AuthOrHomeScreen extends StatelessWidget {
  const AuthOrHomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    Auth auth = Provider.of(context);

    return FutureBuilder(
      future: auth.tryAutoLogin(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        } else if (snapshot.error != null) {
          return Center(
            child: Text('Ocorreu um erro! Contate o Administrador do sistema.'),
          );
        } else {
          return auth.isAuth ? ProductsOverViewScreen() : AuthScreen();
        }
      },
    );
  }
}
