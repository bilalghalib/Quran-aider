import 'package:flutter/material.dart';
import 'package:quran_aider/models/chapter.dart';
import 'package:quran_aider/screens/verse_memorization_screen.dart';

class ChapterSelectionScreen extends StatelessWidget {
  final Chapter chapter;

  const ChapterSelectionScreen({super.key, required this.chapter});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: Colors.black,
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                'Bismillah',
                style: TextStyle(fontSize: 48, color: Colors.white),
              ),
              const SizedBox(height: 20),
              Text(
                chapter.name,
                style: const TextStyle(fontSize: 24, color: Colors.white),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) =>
                          VerseMemorizationScreen(chapter: chapter),
                    ),
                  );
                },
                child: const Text('Start Memorization'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
