import 'package:virtual_store/models/auth.dart';
import 'package:virtual_store/utils/routes/app_routes.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class MainDrawer extends StatelessWidget {
  const MainDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: Column(
        children: [
          AppBar(
            title: const Text('Bem Vindo!'),
            automaticallyImplyLeading: false,
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.shop),
            title: const Text('Loja'),
            onTap: () => Navigator.of(context).pushReplacementNamed(
              AppRoutes.AUTH_OR_HOME,
            ),
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.payment),
            title: const Text('Pedidos'),
            //Fade transition
            // onTap: () => Navigator.of(context).pushReplacement(
            //   CustomRoute(builder: (context) => OrdersScreen()),
            // ),
            onTap: () => Navigator.of(context).pushReplacementNamed(
              AppRoutes.ORDERS,
            ),
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.manage_search),
            title: const Text('Gerenciar Produtos'),
            onTap: () => Navigator.of(context).pushReplacementNamed(
              AppRoutes.PRODUCTS,
            ),
          ),
          const Divider(),
          ListTile(
              leading: const Icon(Icons.exit_to_app),
              title: const Text('Logout'),
              onTap: () {
                Provider.of<Auth>(
                  context,
                  listen: false,
                ).logout();
                Navigator.of(context).pushReplacementNamed(AppRoutes.AUTH_OR_HOME);
              }),
          const Divider(),
        ],
      ),
    );
  }
}
