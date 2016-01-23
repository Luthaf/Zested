/* Zested, an offline editor for Zeste de Savoir
Copyright (C) 2015-2016 Luthaf - Licence MIT */

#include "speller.hpp"

Speller::Speller(const std::string dictspath):
    hunspell((dictspath + "/fr.aff").c_str(), (dictspath + "/fr.dic").c_str()) {}


bool Speller::check(const std::string& word) {
    return hunspell.spell(word.c_str()) != 0;
}

std::vector<std::string> Speller::suggest(const std::string& word) {
    char** suggested;
    size_t n_suggested = hunspell.suggest(&suggested, word.c_str());

    std::vector<std::string> res(n_suggested);
    for (size_t i=0; i<n_suggested; i++) {
        res[i] = std::string(suggested[i]);
    }

    hunspell.free_list(&suggested, n_suggested);
    return res;
}
