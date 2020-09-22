# -*- coding: utf-8 -*-

import math

from openfisca_france.model.base import *
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.base import apply_bareme_for_relevant_type_sal


class allocations_temporaires_invalidite(Variable):
    value_type = float
    entity = Individu
    label = "Allocations temporaires d'invalidité (ATI, fonction publique et collectivités locales)"
    definition_period = MONTH
    # patronale, non-contributive

    def formula(individu, period, parameters):
        assiette_cotisations_sociales_public = individu('assiette_cotisations_sociales_public', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        categorie_salarie = individu('categorie_salarie', period)
        _P = parameters(period)

        base = assiette_cotisations_sociales_public
        cotisation_etat = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur,
            bareme_name = "ati",
            base = base,
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )
        cotisation_collectivites_locales = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur,
            bareme_name = "atiacl",
            base = base,
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )
        return cotisation_etat + cotisation_collectivites_locales


class assiette_cotisations_sociales_public(Variable):
    value_type = float
    entity = Individu
    label = "Assiette des cotisations sociales des agents titulaires de la fonction publique"
    definition_period = MONTH
    # TODO: gestion des heures supplémentaires

    def formula(individu, period, parameters):
        remuneration_principale = individu('remuneration_principale', period)
        # primes_fonction_publique = individu('primes_fonction_publique', period)
        # indemnite_residence = individu('indemnite_residence', period)
        categorie_salarie = individu('categorie_salarie', period)
        public = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )

        assiette = public * (
            remuneration_principale
            # + not_(titulaire) * (indemnite_residence + primes_fonction_publique)
            )
        return assiette


# sft dans assiette csg et RAFP et Cotisation exceptionnelle de solidarité et taxe sur les salaires
# primes dont indemnites de residences idem sft
# avantages en nature contrib exceptionnelle de solidarite, RAFP, CSG, CRDS.


class contribution_exceptionnelle_solidarite(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation exceptionnelle au fonds de solidarité (salarié)"
    definition_period = MONTH
    end = '2017-12-31'
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006072050&idArticle=LEGIARTI000006903878&dateTexte=&categorieLien=cid"

    def formula(individu, period, parameters):
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        hsup = individu('hsup', period)
        categorie_salarie = individu('categorie_salarie', period)
        indemnite_residence = individu('indemnite_residence', period)
        primes_fonction_publique = individu('primes_fonction_publique', period)
        rafp_salarie = individu('rafp_salarie', period)
        pension_civile_salarie = individu('pension_civile_salarie', period)
        cotisations_salariales_contributives = individu('cotisations_salariales_contributives', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        salaire_de_base = individu('salaire_de_base', period)
        supplement_familial_traitement = individu('supplement_familial_traitement', period)
        # Assujettis
        parameters = parameters(period)
        seuil_assujetissement_fds = compute_seuil_fds(parameters)
        concernes = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            + (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)
            )
        remuneration_brute = (
            traitement_indiciaire_brut
            + salaire_de_base
            + indemnite_residence
            - hsup
            )
        assujettis = concernes * (remuneration_brute > seuil_assujetissement_fds)
        # Pour le calcul de l'assiette, on déduit de la rémunaration brute
        #  - toutes les cotisations de sécurité sociale obligatoires
        #  - les prélèvements pour pension
        #  - et, le cas échéant, les prélèvements au profit des régimes de retraite complémentaire obligatoires.
        # Soit:
        #  - pour les titutlaires, les pensions
        #  - les non titulaires, les cotisations sociales contributives (car pas de cotisations non contributives pour les non titulaires de la fonction public)
        deduction = assujettis * (
            + rafp_salarie
            + pension_civile_salarie
            + (categorie_salarie == TypesCategorieSalarie.public_non_titulaire) * cotisations_salariales_contributives
            )
        # Ces déductions sont négatives
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = parameters.cotsoc.cotisations_salarie,
            bareme_name = "excep_solidarite",
            base = assujettis * min_(
                remuneration_brute + supplement_familial_traitement + primes_fonction_publique + deduction,
                parameters.prelevements_sociaux.cotisations_sociales.fds.plafond_base_solidarite,
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )
        return cotisation


class fonds_emploi_hospitalier(Variable):
    value_type = float
    entity = Individu
    label = "Fonds pour l'emploi hospitalier (employeur)"
    definition_period = MONTH

    def formula(individu, period, parameters):
        assiette_cotisations_sociales_public = individu('assiette_cotisations_sociales_public', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        categorie_salarie = individu('categorie_salarie', period)
        _P = parameters(period)
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur,
            bareme_name = "feh",
            base = assiette_cotisations_sociales_public,  # TODO: check base
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )
        return cotisation


class ircantec_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Ircantec salarié"
    definition_period = MONTH

    def formula(individu, period, parameters):
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        categorie_salarie = individu('categorie_salarie', period)
        _P = parameters(period)

        ircantec = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie,
            bareme_name = "ircantec",
            base = assiette_cotisations_sociales,
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )
        return ircantec * (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)


class ircantec_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Ircantec employeur"
    definition_period = MONTH

    def formula(individu, period, parameters):
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        categorie_salarie = individu('categorie_salarie', period)
        _P = parameters(period)

        ircantec = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur,
            bareme_name = "ircantec",
            base = assiette_cotisations_sociales,
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )
        return ircantec * (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)


class pension_civile_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Pension civile salarié"
    definition_period = MONTH

    def formula(individu, period, parameters):
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)  # TODO: check nbi
        categorie_salarie = individu('categorie_salarie', period)
        _P = parameters(period)

        sal = _P.cotsoc.cotisations_salarie
        terr_or_hosp = (
            categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale) | (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)

        pension_civile_salarie = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            * sal['public_titulaire_etat']['pension'].calc(traitement_indiciaire_brut)
            + terr_or_hosp * sal['public_titulaire_territoriale']['cnracl1'].calc(traitement_indiciaire_brut)
            )

        return - pension_civile_salarie


class pension_civile_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation patronale pension civile"
    reference = "http://www.ac-besancon.fr/spip.php?article2662"
    definition_period = MONTH

    def formula(individu, period, parameters):
        assiette_cotisations_sociales_public = individu('assiette_cotisations_sociales_public', period)
        # plafond_securite_sociale = individu('plafond_securite_sociale', period)
        categorie_salarie = individu('categorie_salarie', period)
        _P = parameters(period)

        pat = _P.cotsoc.cotisations_employeur

        terr_or_hosp = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            | (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )

        cot_pat_pension_civile = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            * pat['public_titulaire_etat']['pension'].calc(assiette_cotisations_sociales_public)
            + terr_or_hosp
            * pat['public_titulaire_territoriale']['cnracl'].calc(assiette_cotisations_sociales_public)
            )

        return - cot_pat_pension_civile


class rafp_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Part salariale de la retraite additionelle de la fonction publique"
    definition_period = MONTH
    # Part salariale de la retraite additionelle de la fonction publique
    # TODO: ajouter la gipa qui n'est pas affectée par le plafond d'assiette

    def formula_2005_01_01(individu, period, parameters):
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        categorie_salarie = individu('categorie_salarie', period)
        primes_fonction_publique = individu('primes_fonction_publique', period)
        supplement_familial_traitement = individu('supplement_familial_traitement', period)
        indemnite_residence = individu('indemnite_residence', period)
        _P = parameters(period)

        eligible = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )

        plaf_ass = _P.cotsoc.sal.fonc.etat.rafp_plaf_assiette
        base_imposable = primes_fonction_publique + supplement_familial_traitement + indemnite_residence
        assiette = min_(base_imposable, plaf_ass * traitement_indiciaire_brut * eligible)
        # Même régime pour les fonctions publiques d'Etat et des collectivité locales
        rafp_salarie = eligible * _P.cotsoc.cotisations_salarie.public_titulaire_etat['rafp'].calc(assiette)
        return -rafp_salarie


class rafp_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Part patronale de la retraite additionnelle de la fonction publique"
    definition_period = MONTH

    # TODO: ajouter la gipa qui n'est pas affectée par le plafond d'assiette
    def formula_2005_01_01(individu, period, parameters):
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        categorie_salarie = individu('categorie_salarie', period)
        primes_fonction_publique = individu('primes_fonction_publique', period)
        supplement_familial_traitement = individu('supplement_familial_traitement', period)
        indemnite_residence = individu('indemnite_residence', period)
        _P = parameters(period)

        eligible = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )

        plaf_ass = _P.cotsoc.sal.fonc.etat.rafp_plaf_assiette
        base_imposable = primes_fonction_publique + supplement_familial_traitement + indemnite_residence
        assiette = min_(base_imposable, plaf_ass * traitement_indiciaire_brut * eligible)
        bareme_rafp = _P.cotsoc.cotisations_employeur.public_titulaire_etat['rafp']
        rafp_employeur = eligible * bareme_rafp.calc(assiette)
        return - rafp_employeur


def compute_seuil_fds(parameters):
    '''
    Calcule le seuil mensuel d'assujetissement à la contribution au fond de solidarité
    '''
    fds = parameters.prelevements_sociaux.cotisations_sociales.fds
    pt_ind_mensuel = fds.valeur_annuelle_point_fp / 12
    seuil_mensuel = math.floor((pt_ind_mensuel * fds.indice_majore_de_reference))  # TODO improve
    return seuil_mensuel
