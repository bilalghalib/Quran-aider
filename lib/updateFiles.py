import os

# Step 1: Parsing the input text
def parse_text(input_text):
    files_content = {}
    current_file = None
    lines = input_text.split('\n')
    for line in lines:
        if line.startswith('//'):
            current_file = line.strip().replace('// ', '').strip()
            files_content[current_file] = ''
        elif current_file:
            files_content[current_file] += line + '\n'
    return files_content

# Step 4: File operations - Updating files in the directory
def update_files(base_path, files_content):
    for relative_path, content in files_content.items():
        full_path = os.path.join(base_path, relative_path)
        directory = os.path.dirname(full_path)
        
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)
        
        # Confirmation before writing to the file
        confirm = input(f'Update {full_path}? [y/N] ')
        if confirm.lower() == 'y':
            with open(full_path, 'w') as file:
                file.write(content)
                print(f'Updated {full_path}')
        else:
            print(f'Skipped updating {full_path}')

# Main function to control the flow
def main(input_text, base_path):
    files_content = parse_text(input_text)
    print("Parsed content:")
    for filename, content in files_content.items():
        print(f'Filename: {filename} - Content starts with: {content[:30]}...')  # Show preview of the content
    update_files(base_path, files_content)

# Example usage
input_text = """
// main.dart
import 'package:flutter/material.dart';
import 'package:quran_memorization_app/screens/home_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Quran Memorization',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        fontFamily: 'Arial',
      ),
      home: const HomeScreen(),
    );
  }
}

// verse.dart
class Verse {
  final int verseNumber;
  final String arabicText;
  final String englishTranslation;

  Verse({
    required this.verseNumber,
    required this.arabicText,
    required this.englishTranslation,
  });
}

// chapter.dart
class Chapter {
  final int number;
  final String name;
  final List<Verse> verses;

  Chapter({required this.number, required this.name, required this.verses});
}

// verse_memorization_screen.dart
import 'package:flutter/material.dart';
import 'package:quran_memorization_app/models/chapter.dart';
import 'package:quran_memorization_app/models/verse.dart';
import 'package:quran_memorization_app/services/quran_data_service.dart';
import 'package:audioplayers/audioplayers.dart';

class VerseMemorizationScreen extends StatefulWidget {
  final Chapter chapter;

  const VerseMemorizationScreen({Key? key, required this.chapter})
      : super(key: key);

  @override
  _VerseMemorizationScreenState createState() =>
      _VerseMemorizationScreenState();
}

class _VerseMemorizationScreenState extends State<VerseMemorizationScreen>
    with SingleTickerProviderStateMixin {
  int currentVerseIndex = 0;
  String displayedText = '';
  late AudioPlayer audioPlayer;
  late AnimationController _animationController;
  late Animation<double> _animation;
  bool isLongPressActive = false;
  bool isAudioPlaying = false;

  @override
  void initState() {
    super.initState();
    audioPlayer = AudioPlayer();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 500),
      vsync: this,
    );
    _animation = Tween<double>(begin: 0, end: 1).animate(_animationController);
  }

  @override
  void dispose() {
    audioPlayer.dispose();
    _animationController.dispose();
    super.dispose();
  }

  void revealWords(String text) {
    if (!isLongPressActive) return;

    var words = text.split(' ');
    int wordIndex = 0;

    _animationController.reset();
    _animationController.forward().whenComplete(() {
      if (wordIndex < words.length) {
        setState(() {
          displayedText +=
              (displayedText.isEmpty ? '' : ' ') + words[wordIndex];
          wordIndex++;
        });
        _animationController.reset();
        _animationController.forward();
      }
    });
  }

  void showTranslation(String translation) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('English Translation'),
          content: Text(translation),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Close'),
            ),
          ],
        );
      },
    );
  }

  void playAudio(Verse verse) async {
    if (isAudioPlaying) {
      await audioPlayer.stop();
      setState(() {
        isAudioPlaying = false;
      });
    } else {
      final audioPath =
          'data/Abdullah_Basfar_64kbps/${verse.verseNumber.toString().padLeft(3, '0')}000.mp3';
      await audioPlayer.play(DeviceFileSource(audioPath));
      setState(() {
        isAudioPlaying = true;
      });
      audioPlayer.onPlayerCompletion.listen((event) {
        setState(() {
          isAudioPlaying = false;
        });
      });
    }
  }

  void navigateVerse(int offset) {
    setState(() {
      currentVerseIndex = (currentVerseIndex + offset)
          .clamp(0, widget.chapter.verses.length - 1) as int;
      displayedText = '';
    });
  }

  @override
  Widget build(BuildContext context) {
    final verse = widget.chapter.verses[currentVerseIndex];

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.chapter.name),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: GestureDetector(
        onLongPressStart: (_) {
          setState(() {
            isLongPressActive = true;
          });
          revealWords(verse.arabicText);
        },
        onLongPressEnd: (_) {
          setState(() {
            isLongPressActive = false;
          });
        },
        onDoubleTap: () => showTranslation(verse.englishTranslation),
        child: Container(
          color: Colors.black,
          child: Stack(
            children: [
              Center(
                child: FadeTransition(
                  opacity: _animation,
                  child: Text(
                    displayedText,
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 28, color: Colors.white),
                  ),
                ),
              ),
              Positioned(
                bottom: 20,
                right: 20,
                child: Text(
                  'Verse ${verse.verseNumber}',
                  style: const TextStyle(fontSize: 16, color: Colors.white),
                ),
              ),
              Positioned(
                bottom: 20,
                left: 20,
                child: Row(
                  children: [
                    ElevatedButton(
                      onPressed: () => navigateVerse(-1),
                      child: const Icon(Icons.arrow_back),
                    ),
                    const SizedBox(width: 10),
                    ElevatedButton(
                      onPressed: () => navigateVerse(1),
                      child: const Icon(Icons.arrow_forward),
                    ),
                    const SizedBox(width: 10),
                    ElevatedButton(
                      onPressed: () => playAudio(verse),
                      child: Text(isAudioPlaying ? 'Stop Audio' : 'Play Audio'),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// home_screen.dart
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

// quran_data_service.dart
import 'package:flutter/services.dart' show rootBundle;
import 'package:quran_memorization_app/models/chapter.dart';
import 'package:quran_memorization_app/models/verse.dart';
import 'package:xml/xml.dart';
import 'dart:math';

class QuranDataService {
  static Future<List<Chapter>> getChapters() async {
    List<Chapter> chapters = [];
    try {
      // Assuming there are 114 chapters in total
      for (int i = 1; i <= 114; i++) {
        String chapterFileName = i.toString().padLeft(3, '0');
        String chapterDataPath =
            'data/XML/Arabic/Quran_Arabic_$chapterFileName.xml';
        String chapterData = await rootBundle.loadString(chapterDataPath);
        XmlDocument chapterXml = XmlDocument.parse(chapterData);
        XmlElement? chapterElement =
            chapterXml.findAllElements('sura').firstOrNull;

        if (chapterElement != null) {
          String? idAttr = chapterElement.getAttribute('id');
          String? nameAttr = chapterElement.getAttribute('name');
          if (idAttr == null) {
            print('Missing "id" attribute in chapter element: $chapterElement');
            continue; // Skip this element
          }
          int number = int.parse(idAttr);
          String name =
              nameAttr ?? 'Chapter $number'; // Use a default name if missing

          List<Verse> verses = await getVerses(number);
          chapters.add(Chapter(number: number, name: name, verses: verses));
        }
      }
      return chapters;
    } catch (e) {
      print('Error loading chapters: $e');
      throw Exception('Failed to load chapters');
    }
  }

  static Future<List<Verse>> getVerses(int chapterNumber) async {
    try {
      final arabicData = await rootBundle.loadString(
          'data/XML/Arabic/Quran_Arabic_${chapterNumber.toString().padLeft(3, '0')}.xml');
      final englishData = await rootBundle.loadString(
          'data/XML/English/Quran_Translation_Shakir_${chapterNumber.toString().padLeft(3, '0')}.xml');

      final arabicXml = XmlDocument.parse(arabicData);
      final englishXml = XmlDocument.parse(englishData);

      final arabicVerseElements = arabicXml.findAllElements('aya');
      final englishVerseElements = englishXml.findAllElements('aya');

      List<Verse> verses = [];

      final minLength =
          min(arabicVerseElements.length, englishVerseElements.length);
      for (int i = 0; i < minLength; i++) {
        final arabicVerseElement = arabicVerseElements.elementAt(i);
        final englishVerseElement = englishVerseElements.elementAt(i);

        final verseNumber = int.parse(arabicVerseElement.getAttribute('id')!);
        final arabicText = arabicVerseElement.getAttribute('text')!;
        final englishTranslation = englishVerseElement.text;

        verses.add(Verse(
          verseNumber: verseNumber,
          arabicText: arabicText,
          englishTranslation: englishTranslation,
        ));
      }

      return verses;
    } catch (e) {
      print('Error loading verses for chapter $chapterNumber: $e');
      throw Exception('Failed to load verses for chapter $chapterNumber');
    }
  }
}
"""
base_path = './lib'

main(input_text, base_path)
