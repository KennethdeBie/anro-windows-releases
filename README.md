# Anro Metadata Importer — Windows-releases

Dit is het gratis openbare distributiekanaal voor Anro Metadata Importer op Windows x64. De ontwikkelrepository blijft privé. Deze repository bevat distributiedocumentatie, releasegereedschap en de gepubliceerde installer-/updatebestanden; geen productbroncode, credentials of gebruikersdata.

## Eerste automatische-updatetest

1. Installeer één keer de [bootstrapinstaller 0.2.2](https://github.com/KennethdeBie/anro-windows-releases/releases/download/v0.2.2/Anro-Metadata-Importer-0.2.2-x64-Setup.exe) onder hetzelfde Windows-profiel.
2. Open Instellingen. De app moet de hogere versie 0.2.3 vinden en downloaden. Zo nodig: Controleren op updates.
3. Kies Update veilig installeren. De huidige verwerking wordt eerst afgerond.
4. Controleer na herstart versie 0.2.3, accounts, DEMO/LIVE, opgeslagen-key-status, databases, opdrachten en historie.

Installeer voor deze A→B-test niet meteen 0.2.3; dan is er geen hogere testversie beschikbaar. Oudere installers zonder GitHub-updateadres vereisen nog één handmatige bootstrapinstallatie. Daarna haalt de app hogere stabiele releases zelf op, zonder GitHub-login of token.

De builds zijn momenteel niet code-ondertekend; Windows kan een SmartScreen-melding tonen. Accounts, SQLite-data en via Windows DPAPI versleutelde CCV-keys blijven op de eigen pc. Backup/herstel en LIVE-productwijzigingen worden lokaal beheerd; deel API-keys nooit via GitHub.

## Releases publiceren

Elke release bestaat uit exact de Windows-installer, bijbehorende blockmap en latest.yml. De Windows-build en packaged smoke moeten in de privé-bronrepository geslaagd zijn.

Een maintainer met GitHub CLI-toegang kan het openbare publicatieworkflow starten met:

```sh
python3 tools/dispatch-release.py <succesvol-Windows-run-ID> <versie>
```

Het hulpmiddel controleert het geslaagde bronrun-resultaat en geeft alleen een kortlevende, read-only GitHub-downloadlink voor het geselecteerde installerartifact door. Het accounttoken blijft in het lokale API/CLI-proces en wordt niet doorgegeven of verpakt. De openbare Actions-job gebruikt zijn eigen repository-scoped GITHUB_TOKEN voor upload, valideert versienummer, de drie exacte bestanden, bestandsgrootte en SHA512, uploadt naar een draft en publiceert pas daarna een complete hogere release. Geen permanente cross-repository publishingtoken nodig voor deze maintainerflow. Bestaande releases worden niet overschreven.

Volledig automatisch dispatchen vanuit de privé-CI vereist afzonderlijk beperkte GitHub App-/CI-dispatchbevoegdheid op deze repository; die bevoegdheid hoort nooit in de Windows-app.

## Vertrouwen en herstel

Download uitsluitend uit deze repository. Checksums beschermen downloads tegen corruptie; unsigned builds vertrouwen daarnaast op GitHub/HTTPS en toegangsbeheer van de releaserepository. Herstel een foutieve release bij voorkeur met een hogere herstelversie. Er worden nooit automatisch downgrades uitgevoerd.

De installer bevat openbaar downloadbare applicatiecode. De ontwikkelrepository zelf wordt niet openbaar gemaakt. De source-archives van deze distributierepository bevatten alleen de distributiedocumentatie en publicatiegereedschappen.
