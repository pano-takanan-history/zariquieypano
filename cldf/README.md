<a name="ds-cldfmetadatajson"> </a>

# Wordlist CLDF dataset for Pano languages.

**CLDF Metadata**: [cldf-metadata.json](./cldf-metadata.json)

**Sources**: [sources.bib](./sources.bib)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF Wordlist](http://cldf.clld.org/v1.0/terms.rdf#Wordlist)
[dc:license](http://purl.org/dc/terms/license) | https://creativecommons.org/licenses/by/4.0/
[dcat:accessURL](http://www.w3.org/ns/dcat#accessURL) | https://github.com/pano-takanan-history/zariquieypano
[prov:wasDerivedFrom](http://www.w3.org/ns/prov#wasDerivedFrom) | <ol><li><a href="https://github.com/pano-takanan-history/zariquieypano/tree/v0.4">pano-takanan-history/zariquieypano  v0.4</a></li><li><a href="https://github.com/glottolog/glottolog/tree/v5.3">Glottolog  v5.3</a></li><li><a href="https://github.com/concepticon/concepticon-data/tree/v3.4.0">Concepticon  v3.4.0</a></li><li><a href="https://github.com/cldf-clts/clts/tree/v2.3.0">CLTS  v2.3.0</a></li></ol>
[prov:wasGeneratedBy](http://www.w3.org/ns/prov#wasGeneratedBy) | <ol><li><strong>lingpy-rcParams</strong>: <a href="./lingpy-rcParams.json">lingpy-rcParams.json</a></li><li><strong>python</strong>: 3.14.7</li><li><strong>python-packages</strong>: <a href="./requirements.txt">requirements.txt</a></li></ol>
[rdf:ID](http://www.w3.org/1999/02/22-rdf-syntax-ns#ID) | zariquieypano
[rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type) | http://www.w3.org/ns/dcat#Distribution


## <a name="table-formscsv"></a>Table [forms.csv](./forms.csv)

CustomLexeme(ID: str, Form: str, Value: str, Language_ID: str, Parameter_ID: str, Local_ID: str | None = None, Segments: list[str] = <factory>, Graphemes: list[str] | None = None, Profile: str | None = None, Source: list[str] = <factory>, Comment: str | None = None, Cognacy: str | None = None, Loan: bool | None = None, Partial_Cognacy: Optional[__annotationlib_name_1__] = None, Alignment: Optional[__annotationlib_name_2__] = None, Morphemes: Optional[__annotationlib_name_3__] = None, Note: Optional[__annotationlib_name_4__] = None)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF FormTable](http://cldf.clld.org/v1.0/terms.rdf#FormTable)
[dc:extent](http://purl.org/dc/terms/extent) | 4265


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Local_ID](http://purl.org/dc/terms/identifier) | `string` | 
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | References [languages.csv::ID](#table-languagescsv)
[Parameter_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | References [parameters.csv::ID](#table-parameterscsv)
[Value](http://cldf.clld.org/v1.0/terms.rdf#value) | `string` | 
[Form](http://cldf.clld.org/v1.0/terms.rdf#form) | `string` | 
[Segments](http://cldf.clld.org/v1.0/terms.rdf#segments) | list of `string` (separated by ` `) | 
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
`Cognacy` | `string` | 
`Loan` | `boolean` | 
`Graphemes` | `string` | 
`Profile` | `string` | 
`Partial_Cognacy` | `string` | 
`Alignment` | `string` | 
`Morphemes` | `string` | 
`Note` | `string` | 

## <a name="table-languagescsv"></a>Table [languages.csv](./languages.csv)

CustomLanguage(ID: str = '', Name: str | None = None, ISO639P3code: str | None = None, Glottocode: str | None = None, Macroarea: str | None = None, Latitude: float | None = None, Longitude: float | None = None, Glottolog_Name: str | None = None, Family: str | None = None, SubGroup: Optional[__annotationlib_name_1__] = None, SourceDate: Optional[__annotationlib_name_2__] = None, Source: Optional[__annotationlib_name_3__] = None)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF LanguageTable](http://cldf.clld.org/v1.0/terms.rdf#LanguageTable)
[dc:extent](http://purl.org/dc/terms/extent) | 30


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Glottocode](http://cldf.clld.org/v1.0/terms.rdf#glottocode) | `string` | 
`Glottolog_Name` | `string` | 
[ISO639P3code](http://cldf.clld.org/v1.0/terms.rdf#iso639P3code) | `string` | 
[Macroarea](http://cldf.clld.org/v1.0/terms.rdf#macroarea) | `string` | 
[Latitude](http://cldf.clld.org/v1.0/terms.rdf#latitude) | `decimal`<br>&ge; -90<br>&le; 90 | 
[Longitude](http://cldf.clld.org/v1.0/terms.rdf#longitude) | `decimal`<br>&ge; -180<br>&le; 180 | 
`Family` | `string` | 
`SubGroup` | `string` | 
`SourceDate` | `string` | 
`Source` | `string` | 

## <a name="table-parameterscsv"></a>Table [parameters.csv](./parameters.csv)

CustomConcept(ID: str | None = '', Name: str | None = '', Concepticon_ID: str | None = None, Concepticon_Gloss: str | None = None, Spanish_Gloss: Optional[__annotationlib_name_1__] = None)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ParameterTable](http://cldf.clld.org/v1.0/terms.rdf#ParameterTable)
[dc:extent](http://purl.org/dc/terms/extent) | 181


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Concepticon_ID](http://cldf.clld.org/v1.0/terms.rdf#concepticonReference) | `string` | 
`Concepticon_Gloss` | `string` | 
`Spanish_Gloss` | `string` | 
