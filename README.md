# ESP32 Cam - Application Windows

Une application Windows complète pour contrôler et capturer des images/vidéos à partir d'une caméra ESP32, avec interface graphique intuitive et sauvegarde locale.

## 📋 Table des matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Dépendances](#dépendances)
- [Captures d'écran](#captures-décran)
- [Matériel utilisé](#matériel-utilisé)
- [Dépannage](#dépannage)
- [Auteur](#auteur)

## 🎯 Aperçu

Ce projet permet de contrôler une caméra ESP32 via une application Windows desktop. L'application établit une connexion réseau avec le microcontrôleur ESP32 pour capturer des images en temps réel, les afficher dans une interface graphique et les sauvegarder localement sur votre ordinateur.

### Interface graphique
**[Ajouter un screenshot de l'interface principale de l'application ici]**

## ✨ Fonctionnalités

- ✅ **Connexion réseau WiFi** : Se connecte à l'ESP32 via WiFi/IP
- ✅ **Capture d'images** : Capture des photos individuelles à partir de la caméra
- ✅ **Flux vidéo en direct** : Affichage du flux vidéo en temps réel
- ✅ **Sauvegarde locale** : Enregistrement automatique des captures avec horodatage
- ✅ **Interface intuitive** : Application GUI facile à utiliser
- ✅ **Contrôle complet** : Paramètres ajustables pour la caméra
- ✅ **Affichage d'état** : Indication de la connexion et du statut

## 🔧 Prérequis

### Matériel
- **ESP32 avec caméra OV2640** (module ESP32-CAM ou similaire)
- **Ordinateur Windows** (Windows 7, 10, 11 ou supérieur)
- **Connexion réseau WiFi** pour la communication

### Logiciel
- Python 3.7+ (si exécution depuis source)
- OU exécutable fourni (pas besoin d'installer Python)

## 📦 Installation

### Option 1 : Utiliser l'exécutable (Recommandé)

1. Téléchargez le fichier `esp32cam_app.exe` depuis la version release
2. Double-cliquez sur le fichier pour lancer l'application
3. Aucune installation supplémentaire n'est nécessaire

### Option 2 : Exécuter depuis le code source

1. **Clonez le projet** :
   ```bash
   git clone https://github.com/Eliott243/smart-imaging-and-web-basd-camera-.git
   cd ESP32Cam_windows-App-main
   ```

2. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancez l'application** :
   ```bash
   python esp32cam_app.py
   ```

## ⚙️ Configuration

### Configuration du firmware ESP32

1. Programmez votre ESP32 avec le firmware approprié (voir `ESP32_CAM_Controller.spec`)
2. Configurez les paramètres WiFi dans le code de l'ESP32
3. Notez l'adresse IP de votre ESP32

### Configuration de l'application

1. Lancez l'application `esp32cam_app.py`
2. Entrez l'adresse IP de votre ESP32
3. Cliquez sur "Se connecter"
4. L'application établira la connexion

### Paramètres de sauvegarde

Les images capturées sont sauvegardées par défaut dans le répertoire courant avec le format :
```
esp32cam_YYYY-MM-DD_HH-MM-SS.jpg
```

## 🚀 Utilisation

### Interface principale

**[Ajouter un screenshot détaillé de l'interface avec annotations ici]**

### Étapes basiques

1. **Connexion** : Démarrez l'application et connectez-vous à votre ESP32
2. **Aperçu** : Visualisez le flux vidéo en direct
3. **Capture** : Cliquez sur le bouton "Capturer" pour sauvegarder une image
4. **Téléchargement** : Les images sont automatiquement téléchargées et sauvegardées

### Contrôles disponibles

| Bouton | Action |
|--------|--------|
| **Se connecter** | Établit la connexion avec l'ESP32 |
| **Capturer** | Prend une photo et la sauvegarde |
| **Déconnecter** | Ferme la connexion avec l'ESP32 |
| **Paramètres** | Accès aux options avancées |

## 📁 Structure du projet

```
ESP32Cam_windows-App-main/
├── esp32cam_app.py              # Application principale
├── ESP32_CAM_Controller.spec    # Configuration PyInstaller
├── esp32cam_app.spec            # Configuration PyInstaller alternative
├── README.md                    # Ce fichier
├── .gitignore                   # Fichiers ignorés par Git
└── build/                       # Dossier de compilation (non versionné)
```

## 📚 Dépendances

Les dépendances principales sont :

```
opencv-python>=4.5.0
numpy>=1.19.0
requests>=2.25.0
pillow>=8.0.0
tkinter (inclus avec Python)
```

Voir `requirements.txt` pour la liste complète.

## 📸 Captures d'écran

### Vue principale de l'application
![Interface principale]()
**[Ajouter ici un screenshot de l'interface principale]**

### Affichage du flux vidéo
![Flux vidéo]()
**[Ajouter ici un screenshot du flux vidéo en direct]**

### Fenêtre de paramètres
![Paramètres]()
**[Ajouter ici un screenshot des paramètres/options]**

## 🔌 Matériel utilisé

### Module ESP32-CAM
**[Ajouter ici une photo du module ESP32-CAM]**

**Spécifications :**
- Microcontrôleur : ESP32 (WiFi + Bluetooth)
- Caméra : OV2640 (2MP)
- Mémoire : 4MB Flash
- Alimentation : 5V USB

### Assemblage physique
**[Ajouter ici une photo du projet physique assemblé]**

**Composants typiques :**
- Module ESP32-CAM
- Câble USB pour l'alimentation
- Antenne WiFi (intégrée)
- Boîtier de protection (optionnel)

### Schéma de connexion
```
PC (Windows) <--WiFi--> ESP32-CAM
                          |
                          └--- Caméra OV2640
```

## 🔍 Dépannage

### Problème : Impossible de se connecter à l'ESP32

**Solution :**
1. Vérifiez que l'ESP32 est alimenté
2. Assurez-vous que l'ESP32 et le PC sont sur le même réseau WiFi
3. Vérifiez l'adresse IP correcte
4. Vérifiez les paramètres de pare-feu Windows

### Problème : Les images ne s'affichent pas

**Solution :**
1. Vérifiez la connexion réseau
2. Assurez-vous que la caméra est correctement connectée à l'ESP32
3. Essayez de redémarrer l'ESP32
4. Vérifiez les logs de l'application

### Problème : L'application ne démarre pas

**Solution :**
1. Assurez-vous que Python 3.7+ est installé (si exécution depuis source)
2. Vérifiez que toutes les dépendances sont installées
3. Utilisez l'exécutable au lieu du code source

## 📝 Notes importantes

- Les images sont capturées en format JPEG
- La qualité dépend de la caméra ESP32 et de la connexion réseau
- Une connexion stable est recommandée pour le flux vidéo
- L'application enregistre un horodatage précis pour chaque capture

## 🛠️ Développement

### Construire l'exécutable

Pour créer votre propre exécutable Windows :

```bash
pyinstaller esp32cam_app.spec
```

L'exécutable sera généré dans le dossier `dist/`.

### Modifier l'application

Le fichier principal `esp32cam_app.py` peut être modifié pour :
- Changer l'interface graphique
- Ajouter de nouvelles fonctionnalités
- Modifier les paramètres de sauvegarde
- Implémenter de nouveaux protocoles de communication

## 📄 Licence

Ce projet est fourni tel quel pour usage personnel et éducatif.

## 👤 Auteur

**Eliott243**
- GitHub : [Eliott243](https://github.com/Eliott243)
- Projet : [Smart Imaging and Web Based Camera](https://github.com/Eliott243/smart-imaging-and-web-basd-camera-)

## 🤝 Contribution

Les suggestions et améliorations sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📮 Support

Pour toute question ou problème :
1. Consultez la section [Dépannage](#dépannage)
2. Vérifiez les issues GitHub existantes
3. Créez une nouvelle issue avec la description détaillée du problème

---

**Dernière mise à jour** : May 2026
**Version** : 1.0.0
