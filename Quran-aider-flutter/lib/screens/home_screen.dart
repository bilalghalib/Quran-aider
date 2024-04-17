import 'package:flutter/material.dart';
import 'package:quran_memorization_app/screens/verse_memorization_screen.dart';
import 'package:quran_memorization_app/services/quran_data_service.dart';
import 'package:quran_memorization_app/models/chapter.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late Future<List<Chapter>> _chaptersData;

  @override
  void initState() {
    super.initState();
    _chaptersData = QuranDataService.getChapters();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Quran Memorization'),
      ),
      body: FutureBuilder<List<Chapter>>(
        future: _chaptersData,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    'Failed to load chapters',
                    style: TextStyle(fontSize: 18, color: Colors.red),
                  ),
                  const SizedBox(height: 10),
                  ElevatedButton(
                    onPressed: () {
                      // Retry loading chapters
                      setState(() {
                        _chaptersData = QuranDataService.getChapters();
                      });
                    },
                    child: const Text('Retry'),
                  ),
                ],
              ),
            );
          } else if (snapshot.hasData) {
            final chapters = snapshot.data!;
            return ListView.builder(
              itemCount: chapters.length,
              itemBuilder: (context, index) {
                final chapter = chapters[index];
                return ListTile(
                  title: Text(chapter.name),
                  subtitle: Text('Chapter ${chapter.number}'),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) =>
                            VerseMemorizationScreen(chapter: chapter),
                      ),
                    );
                  },
                );
              },
            );
          } else {
            return const Center(
              child: Text(
                'No chapters available',
                style: TextStyle(fontSize: 18),
              ),
            );
          }
        },
      ),
    );
  }
}

