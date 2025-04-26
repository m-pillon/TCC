from datetime import datetime
from time import time
from django.db import models


class SleepQuestionnaire(models.Model):
    class Difficulty(models.IntegerChoices):
        NONE = 0, 'Nenhuma dificuldade'
        MILD = 1, 'Um problema leve'
        MODERATE = 2, 'Um problema razoável'
        SEVERE = 3, 'Um grande problema'

        @classmethod
        def get_value(cls, label):
            for value, name in cls.choices:
                if name == label:
                    return value
            return None

    class Quality(models.IntegerChoices):
        VERY_GOOD = 4, 'Muito boa'
        GOOD = 3, 'Boa'
        FAIR = 2, 'Ruim'
        POOR = 1, 'Muito ruim'

        @classmethod
        def get_value(cls, label):
            for value, name in cls.choices:
                if name == label:
                    return value
            return None
    
    class Frequency(models.IntegerChoices): 
        NONE = 0, 'Nenhuma no último mês'
        LESS_THAN_ONCE_A_WEEK = 1, 'Menos de 1 vez/semana'
        ONCE_OR_TWICE_A_WEEK = 2, '1 ou 2 vezes/semana'    
        VERY_OFTEN = 3, '3 ou mais vezes/semana'

        @classmethod
        def get_value(cls, label):
            for value, name in cls.choices:
                if name == label:
                    return value
            return None

    class Partner(models.IntegerChoices):
        NO = 0, 'Não'
        PARTNER_IN_OTHER_ROOM = 1, 'Parceiro ou colega, mas em outro quarto'
        PARTNER_IN_SAME_ROOM = 2, 'Parceiro no mesmo quarto, mas não na mesma cama'
        PARTNER_IN_SAME_BED = 3, 'Parceiro na mesma cama'

        @classmethod
        def get_value(cls, label):
            for value, name in cls.choices:
                if name == label:
                    return value
            return None

    # Basic sleep information
    bedtime = models.TimeField(verbose_name="Hora usual de deitar") # Q1
    time_to_sleep = models.PositiveIntegerField(verbose_name="Minutos para dormir") # Q2
    wakeup_time = models.TimeField(verbose_name="Hora usual de levantar") # Q3
    sleep_hours = models.FloatField(verbose_name="Horas de sono por noite") # Q4
    
    # Sleep difficulties = Q5
    difficulty_falling_asleep = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Não conseguiu adormecer em até 30 minutos"
    )
    difficulty_staying_asleep = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Acordou no meio da noite ou de manhã cedo"
    )
    bathroom_visits = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Precisou levantar para ir ao banheiro"
    )
    breathing_difficulty = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Não conseguiu respirar confortavelmente"
    )
    coughing_snoring = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Tossiu ou roncou forte"
    )
    felt_cold = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Sentiu muito frio"
    )
    felt_hot = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Sentiu muito calor"
    )
    bad_dreams = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Teve sonhos ruins"
    )
    pain = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Teve dor"
    )
    other_reason = models.TextField(
        blank=True, null=True,
        verbose_name="Outra(s) razão(ões), por favor descreva"
    )
    other_reason_frequency = models.IntegerField(
        max_length=1, choices=Frequency.choices, blank=True, null=True,
        verbose_name="Frequência da outra razão"
    )
    
    # General sleep evaluation = Q6, Q7, Q8, Q9
    sleep_quality = models.IntegerField(
        max_length=1, choices=Quality.choices,
        verbose_name="Qualidade geral do sono"
    )
    medication_use = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Uso de medicamento para dormir"
    )
    daytime_sleepiness = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Dificuldade de ficar acordado durante atividades"
    )
    enthusiasm_difficulty = models.IntegerField(
        max_length=1, choices=Difficulty.choices,
        verbose_name="Dificuldade em manter entusiasmo"
    )
    
    # Partner information
    has_partner = models.IntegerField(
        max_length=1, choices=Partner.choices,
        verbose_name="Tem parceiro/colega de quarto?"
    )
    partner_snoring = models.IntegerField(
        max_length=1, choices=Frequency.choices, blank=True, null=True,
        verbose_name="Ronco forte (observado por parceiro)"
    )
    partner_breathing_pauses = models.IntegerField(
        max_length=1, choices=Frequency.choices, blank=True, null=True,
        verbose_name="Longas paradas na respiração (observado por parceiro)"
    )
    partner_leg_movements = models.IntegerField(
        max_length=1, choices=Frequency.choices, blank=True, null=True,
        verbose_name="Contrações/puxões nas pernas (observado por parceiro)"
    )
    partner_confusion = models.IntegerField(
        max_length=1, choices=Frequency.choices, blank=True, null=True,
        verbose_name="Episódios de desorientação (observado por parceiro)"
    )
    partner_other_issues = models.TextField(
        blank=True, null=True,
        verbose_name="Outras alterações observadas (descreva)"
    )
    partner_other_frequency = models.IntegerField(
        max_length=1, choices=Frequency.choices, blank=True, null=True,
        verbose_name="Frequência das outras alterações"
    )
    
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Questionário de sono de {self.created_at.date()}"
            
    def calculate_total_score(self):
        """
        DURAT + DISTB + LATEN + DAYDYS + HSE + SLPQUAL + MEDS Minimum
        Score = 0 (better); Maximum Score = 21 (worse) 
        """
        duration_score = self._get_duration_score()
        difficulty_score = self._get_difficulty_score()
        latent_score = self._get_latent_score()
        daytime_score = self._get_daytime_score()
        sleep_efficiency_score = self._get_sleep_efficiency_score()
        sleep_quality_score = int(getattr(self, "sleep_quality"))
        medication_use_score = int(getattr(self, "medication_use"))

        total = duration_score + difficulty_score + latent_score + daytime_score + sleep_efficiency_score + sleep_quality_score + medication_use_score

        return total
    
    def _get_duration_score(self):
        """
        IF Q4 > 7, THEN set value to 0
        IF Q4 < 7 and > 6, THEN set value to 1
        IF Q4 < 6 and > 5, THEN set value to 2
        IF Q4 < 5, THEN set value to 3
        Minimum Score = 0 (better); Maximum Score = 3 (worse) 
        """
        if float(self.sleep_hours) >= 7:
            return 0
        elif 6 < float(self.sleep_hours) < 7:
            return 1
        elif 5 < float(self.sleep_hours) <= 6:
            return 2
        else:
            return 3
    
    def _get_difficulty_score(self):
        """
        IF Q5COM = 0, THEN set value to 0
        IF Q5COM > 1 and < 9, THEN set value to 1
        IF Q5COM > 9 and < 18, THEN set value to 2
        IF Q5COM > 18, THEN set value to 3
        Minimum Score = 0 (better); Maximum Score = 3 (worse)
        """
        difficulty_score = self._sum_difficulty_scores()
        
        if difficulty_score == 0:
            return 0
        elif 0 < difficulty_score < 9:
            return 1
        elif 9 <= difficulty_score < 18:
            return 2
        else:
            return 3

    def _get_new_latent_score(self):
        """
        First, recode Q2 into Q2new thusly:
        IF Q2 > 0 and < 15, THEN set value of Q2new to 0
        IF Q2 > 15 and < 30, THEN set value of Q2new to 1
        IF Q2 > 30 and < 60, THEN set value of Q2new to 2
        IF Q2 > 60, THEN set value of Q2new to 3 
        """
        if self.time_to_sleep is None:
            return None
        
        if 0 < self.time_to_sleep < 15:
            return 0
        elif 15 <= self.time_to_sleep < 30:
            return 1
        elif 30 <= self.time_to_sleep < 60:
            return 2
        else:
            return 3
        
    def _get_latent_score(self):
        """
        Next
        IF Q5a + Q2new = 0, THEN set value to 0
        IF Q5a + Q2new >= 1 and <= 2, THEN set value to 1
        IF Q5a + Q2new >= 3 and <= 4, THEN set value to 2
        IF Q5a + Q2new >= 5 and <= 6, THEN set value to 3
        Minimum Score = 0 (better); Maximum Score = 3 (worse) 
        """
        if int(getattr(self, "difficulty_falling_asleep")) + self._get_new_latent_score() == 0:
            return 0
        elif 1 <= (int(getattr(self, "difficulty_falling_asleep")) + self._get_new_latent_score()) <= 2:
            return 1
        elif 3 <= (int(getattr(self, "difficulty_falling_asleep")) + self._get_new_latent_score()) <= 4:
            return 2
        else:
            return 3

    def _get_daytime_score(self):
        """
        IF Q8 + Q9 = 0, THEN set value to 0
        IF Q8 + Q9 > 1 and < 2, THEN set value to 1
        IF Q8 + Q9 > 3 and < 4, THEN set value to 2
        IF Q8 + Q9 > 5 and < 6, THEN set value to 3
        Minimum Score = 0 (better); Maximum Score = 3 (worse)
        """
        daytime_score = self._sum_daytime_scores()
        
        if daytime_score == 0:
            return 0
        elif 1 <= daytime_score <= 2:
            return 1
        elif 3 <= daytime_score <= 4:
            return 2
        else:
            return 3

    def _get_sleep_efficiency_score(self):
        """
        Diffsec = Diffsec = Difference in seconds between times for Bed Time (Q1) and
        Getting Up Time (Q3).
        Diffhour = Absolute value of diffsec / 3600
        newtib =IF diffhour > 24, then newtib = diffhour – 24
        IF diffhour < 24, THEN newtib = diffhour
        (NOTE, THE ABOVE JUST CALCULATES THE HOURS BETWEEN BED
        TIME (Q1) AND GETTING UP TIME (Q3)
        tmphse = (Q4 / newtib) * 100
        IF tmphse > 85, THEN set value to 0
        IF tmphse < 85 and > 75, THEN set value to 1
        IF tmphse < 75 and > 65, THEN set value to 2
        IF tmphse < 65, THEN set value to 3
        Minimum Score = 0 (better); Maximum Score = 3 (worse) 
        """
        if self.bedtime is None or self.wakeup_time is None:
            return None
        
        # Calculate the difference in seconds between bedtime and wakeup time
        diffsec = (datetime.combine(datetime.today(), self.wakeup_time) - 
                   datetime.combine(datetime.today(), self.bedtime)).total_seconds()
        
        # Calculate the absolute value of diffsec in hours
        diffhour = abs(diffsec) / 3600

        # Adjust for overnight sleep
        newtib = diffhour - 24 if diffhour > 24 else diffhour
        
        # Calculate sleep efficiency
        tmphse = (self.sleep_hours / newtib) * 100
        
        if tmphse >= 85:
            return 0
        elif 75 <= tmphse < 85:
            return 1
        elif 65 <= tmphse < 75:
            return 2
        else:
            return 3

    def _sum_difficulty_scores(self):
        """Helper method to sum all sleep difficulty scores"""
        difficulty_fields = [
            'difficulty_falling_asleep',
            'difficulty_staying_asleep',
            'bathroom_visits',
            'breathing_difficulty',
            'coughing_snoring',
            'felt_cold',
            'felt_hot',
            'bad_dreams',
            'pain',
            'other_reason_frequency'
        ]
        return sum(
            int(getattr(self, field)) 
            for field in difficulty_fields 
            if getattr(self, field) is not None
        )
    
    def _get_quality_score(self):
        """Helper method for sleep quality component"""
        if self.sleep_quality is None:
            return None
        return (4 - int(self.sleep_quality) + 1)  # Inverted scoring
    
    def _sum_daytime_scores(self):
        """Helper method for daytime impact component"""
        daytime_fields = [
            'daytime_sleepiness',
            'enthusiasm_difficulty'
        ]
        return sum(
            int(getattr(self, field))
            for field in daytime_fields
            if getattr(self, field) is not None
        )

