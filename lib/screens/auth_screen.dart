import 'dart:math';

import 'package:virtual_store/components/auth_form.dart';
import 'package:flutter/material.dart';

class AuthScreen extends StatelessWidget {
  const AuthScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [
                  Color.fromRGBO(147, 52, 185, 0.877),
                  Color.fromRGBO(224, 112, 47, 0.726),
                ],
              ),
            ),
          ),
          Center(
            child: SingleChildScrollView(
              child: Container(
                width: double.infinity,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Container(
                      margin: EdgeInsets.only(
                        bottom: 22,
                      ),
                      padding: EdgeInsets.symmetric(
                        vertical: 10,
                        horizontal: 70,
                      ),
                      //cascade operator '..'
                      transform: Matrix4.rotationZ(-8 * pi / 240)..translate(-10.0),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(20),
                        color: Colors.deepOrange.shade900,
                        boxShadow: [
                          BoxShadow(
                            blurRadius: 8,
                            color: Colors.black45,
                            offset: Offset(0, 4),
                          ),
                        ],
                      ),
                      child: Text(
                        'Loja Virtual',
                        style: TextStyle(
                          fontSize: 45,
                          fontFamily: 'Anton',
                          color: Theme.of(context).primaryTextTheme.headlineMedium?.color,
                        ),
                      ),
                    ),
                    AuthForm(),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
