# yml2curios

[Curios](https://icto.ugent.be/en/manual/curios/teachers) is a web application for online assessment, used a.o. by Ghent University and Ghent University of Applied Sciences (HOGENT). `yml2curios` is a tool that aims to make creating a series of questions easier. The user creates a YAML file containing the questions, and `yml2curios` will create a zip file that can be imported in Curios.

Example:

```yaml
- type: MC4ver
  vraag: In welk land is het coronavirus ontstaan?
  antwoord: China
  afleider1: België
  afleider2: Italië
  afleider3: Antarctica
- type: MC4ver
  vraag: Wat is de officiële naam van het coronavirus?
  antwoord: Covid-19
  afleider1: SARS
  afleider2: influenza
  afleider3: corona
```

Remark that the tool is very limited in scope right now! If you have suggestions or want to cooperate on improving this tool, let me know!