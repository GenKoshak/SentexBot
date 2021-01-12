from googletrans import Translator
import spacy

DEPS = ['nsubj', 'csubj', 'ccomp', 'xcomp', 'dobj', 'iboj', 'pobj', 'npadvmod', 'nummod', 'nmod', 'advmod', 'prep',
        'neg', 'prt', 'advcl', 'acl', 'amod', 'mark', 'attr', 'acomp', 'expl', 'intj', 'conj', 'dative', 'nsubjpass',
        'auxpass', 'compound', 'agent', 'cc']


PASSIVE_DEPS = ['nsubj', 'csubj', 'ccomp', 'xcomp', 'dobj', 'iboj', 'pobj', 'npadvmod', 'nummod', 'nmod', 'advmod',
                'prep', 'neg', 'prt', 'advcl', 'acl', 'amod', 'mark', 'attr', 'acomp', 'expl', 'intj', 'conj',
                'dative', 'nsubjpass', 'auxpass', 'compound', 'agent', 'aux', 'auxpass', 'cc']


def get_pred(token, nlp, voice, intent):
    sent = list()
    phrase = str()
    for tok in token.subtree:
        if tok.dep_ == 'ROOT':
            if intent == 'n':
                pred = 'to ' + tok.lemma_
                sent.append(pred)
            elif intent == 'y':
                aux = ' '.join([tok.orth_ for tok in tok.subtree if tok.dep_ == 'aux' or tok.dep_ == 'ROOT' or
                                tok.dep_ == 'xcomp'])
                sent.append(aux)
        if voice == 'act':
            if tok.dep_ in DEPS:
                phrase = ' '.join([tok.orth_ for tok in tok.subtree])
        if voice == 'pass':
            if tok.dep_ in PASSIVE_DEPS:
                phrase = ' '.join([tok.orth_ for tok in tok.subtree])
        sent_str = ' '.join(i for i in sent)
        add_str = ''
        IN_SENT = nlp.vocab.add_flag(lambda text: text in sent_str.split(' '))
        candidate = nlp(phrase)
        for i in candidate:
            if not i.check_flag(IN_SENT):
                add_str += ' ' + i.text
        sent.append(add_str)
        for i in sent:
            if len(i) == 0:
                sent.remove(i)
    return sent


def get_deps(message, voice, intent):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(message)
    sent = list()
    for token in doc:
        if token.dep_ == 'ROOT':
            sent = get_pred(token, nlp, voice, intent)
        if token.text == '?':
            sent.append(token.text)
    return sent


def get_translation(sentence):
    translation = []
    translator = Translator()
    for i in sentence:
        translated = translator.translate(str(i), dest='ru')
        translation.append(translated.text)
    return translation


# gd = get_deps("I live in Moscow", 'act', 'n')
# print(get_translation(gd))
