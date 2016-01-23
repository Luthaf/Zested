/* Zested, an offline editor for Zeste de Savoir
Copyright (C) 2015-2016 Luthaf - Licence MIT */

#ifndef ZESTED_SPELLER_HPP
#define ZESTED_SPELLER_HPP

#include <string>
#include <vector>

#include <hunspell.hxx>

//! Spell checker class
class Speller {
public:
    //! Create a spell-checker using dicts in `dictspath`. The files
    //! `dictspath/fr.aff` and `dictspath/fr.dic` should exist, and
    //! follow Hunspell file format.
    explicit Speller(const std::string dictspath);
    Speller(const Speller&) = delete;
    Speller& operator=(const Speller&) = delete;
    Speller(Speller&&) = default;
    Speller& operator=(Speller&&) = default;

    //! Check wether the word is well spelled
    bool check(const std::string& word);
    //! Get spelling suggestions for a word
    std::vector<std::string> suggest(const std::string& word);
private:
    Hunspell hunspell;
};

#endif
