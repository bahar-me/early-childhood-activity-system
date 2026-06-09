import { Activity } from '../types/activity';
import { TeacherProfile, ClassProfile } from '../types/profile';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Printer, Clock, Users } from 'lucide-react';
import { Capacitor } from '@capacitor/core';
import { toast } from 'sonner';
import { useState } from 'react';
import { PdfGenerator } from '@capgo/capacitor-pdf-generator';
import { Filesystem, Directory } from '@capacitor/filesystem';
import {Share} from '@capacitor/share';

const getSubjectColor = (subject: string) => {
  const colors: Record<string, string> = {
    Math: 'bg-blue-100 text-blue-800 border-blue-300',
    Language: 'bg-purple-100 text-purple-800 border-purple-300',
    Art: 'bg-pink-100 text-pink-800 border-pink-300',
    Science: 'bg-green-100 text-green-800 border-green-300',
    Music: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    Physical: 'bg-orange-100 text-orange-800 border-orange-300',
    'Social-Emotional': 'bg-teal-100 text-teal-800 border-teal-300',
  };
  return colors[subject] || 'bg-gray-100 text-gray-800 border-gray-300';
};

interface ActivityReportProps {
  activities: Activity[];
  teacherProfile: TeacherProfile;
  classProfile: ClassProfile;
  open: boolean;
  onClose: () => void;
  aiExplanation?: {
    summary: string;
    source: string;
    activity_explanations: {
      activity_id: string;
      title: string;
      explanation: string;
      teacher_guidance: string;
      adaptation: string;
    }[];
  } | null;
}

export function ActivityReport({
  activities,
  teacherProfile,
  classProfile,
  open,
  onClose,
  aiExplanation,
}: ActivityReportProps) {
  const [nativeReportHtml, setNativeReportHtml] = useState<string | null>(null);
  const handlePrint = async() => {
    if (!teacherProfile || !classProfile || activities.length === 0) {
      toast.error('Yazdırmak için yeterli bilgiler bulunamadı');
      return;
    }

    const totalDuration = activities.reduce((total, activity) => {
      const durationMap: Record<string, number> = {
        '5-15min': 15,
        '15-30min': 30,
        '30-45min': 45,
        '45-60min': 60,
      };
      return total + (durationMap[activity.duration] || 0);
    }, 0);

    const escapeHtml = (text: string) => {
      return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    };

    const printStyles = `
      @page {
        size: A4;
        margin: 14mm;
      }

      * {
        box-sizing: border-box;
      }

      body {
        font-family: Arial, Helvetica, sans-serif;
        color: #111827;
        background: #ffffff;
        margin: 0;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }

      .report-root {
        width: 100%;
      }

      .cover-page {
        min-height: 260mm;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        border: 2px solid #e5e7eb;
        padding: 40px;
      }

      .cover-title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 28px;
        color: #111827;
      }

      .cover-subtitle {
        font-size: 18px;
        color: #374151;
        margin-bottom: 8px;
      }

      .cover-info {
        margin-top: 36px;
        font-size: 15px;
        line-height: 1.8;
        color: #374151;
      }

      .page-break {
        page-break-before: always;
      }

      .report-title {
        font-size: 28px;
        font-weight: 800;
        margin: 0 0 6px 0;
        color: #111827;
      }

      .report-subtitle {
        font-size: 14px;
        color: #6b7280;
        margin: 0 0 20px 0;
      }

      .top-grid {
        display: flex;
        gap: 16px;
        margin-bottom: 16px;
      }

      .top-column {
        flex: 1;
      }

      .info-card,
      .section-card,
      .activity-card {
        border: 1px solid #d1d5db;
        border-radius: 14px;
        padding: 10px;
        background: #ffffff;
        margin-bottom: 10px;
      }

      .info-card {
        background: #f9fafb;
      }

      .section-title {
        margin: 0 0 12px 0;
        font-size: 18px;
        font-weight: 800;
        color: #111827;
      }

      .meta-list {
        display: grid;
        grid-template-columns: 120px 1fr;
        gap: 8px 12px;
        font-size: 14px;
      }

      .meta-label {
        font-weight: 700;
        color: #111827;
      }

      .meta-value {
        color: #374151;
      }

      .summary-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 14px;
      }

      .summary-item {
        border: 1px solid #dbeafe;
        background: #eff6ff;
        border-radius: 12px;
        padding: 12px;
      }

      .summary-label {
        font-size: 12px;
        color: #4b5563;
        margin-bottom: 4px;
      }

      .summary-value {
        font-size: 22px;
        font-weight: 800;
        color: #111827;
      }

      .badges {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 8px;
      }

      .badge {
        display: inline-block;
        border: 1px solid #d1d5db;
        border-radius: 999px;
        padding: 5px 11px;
        background: #f3f4f6;
        color: #111827;
        font-size: 12px;
        font-weight: 700;
      }

      .activity-card {
        page-break-inside: auto;
        break-inside: auto;
      }

      .activity-title {
        background: #eef2ff;
        border-left: 6px solid #4f46e5;
        padding: 8px 10px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 800;
        margin: 0 0 12px 0;
      }

      .muted {
        color: #4b5563;
        font-size: 12px;
        line-height: 1.35;
      }

      .two-column {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-top: 10px;
      }

      .blue-box {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-left: 5px solid #3b82f6;
        border-radius: 12px;
        padding: 12px;
      }

      .green-box {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        border-left: 5px solid #10b981;
        border-radius: 12px;
        padding: 12px;
      }

      .gray-box {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 10px;
        margin-top: 10px;
      }

      .assessment-box {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        border-left: 5px solid #10b981;
        border-radius: 12px;
        padding: 10px;
        margin-top: 10px;
      }

      .list-title {
        margin: 0 0 8px 0;
        font-size: 14px;
        font-weight: 800;
        color: #111827;
      }

      ul,
      ol {
        margin: 6px 0 0 18px;
        padding: 0;
        color: #374151;
        font-size: 11.5px;
        line-height: 1.35;
      }

      li {
        margin-bottom: 4px;
      }

      .summary-box {
        white-space: pre-line;
        line-height: 1.35;
        font-size: 11.5px;
        color: #374151;
      }

      .footer {
        position: fixed;
        bottom: 6mm;
        left: 0;
        right: 0;
        text-align: center;
        font-size: 11px;
        color: #6b7280;
      }

      @media print {
        .info-card,
        .section-card {
          break-inside: avoid;
          page-break-inside: avoid;
        }

        .activity-card {
          break-inside: auto;
          page-break-inside: auto;
        }
      }
    `;

    const activitiesHtml = activities
      .map((activity, index) => {
        const materials = activity.materials
          .map((item) => `<li>${escapeHtml(item)}</li>`)
          .join('');

        const goals = activity.learningGoals
          .map((item) => `<li>${escapeHtml(item)}</li>`)
          .join('');

        const instructions = activity.instructions
          .map((item) => `<li>${escapeHtml(item)}</li>`)
          .join('');
          
        const assessmentQuestions = (activity.assessmentQuestions || [])
          .map((item) => `<li>${escapeHtml(item)}</li>`)
          .join('');

        return `
          <div class="activity-card ${index > 0 ? 'page-break' : ''}">
            <h3 class="activity-title">${index + 1}. ${escapeHtml(activity.title)}</h3>

            <div class="badges">
              <span class="badge">${escapeHtml(translateSubject(activity.subject))}</span>
              <span class="badge">${escapeHtml(translateDuration(activity.duration))}</span>
              <span class="badge">${escapeHtml(translateGroupSize(activity.groupSize))}</span>
            </div>

            <p class="muted" style="margin-top: 12px;">
              ${escapeHtml(activity.description)}
            </p>

            <div class="two-column">
              <div class="blue-box">
                <div class="list-title">Materyaller</div>
                  <ul>${materials}</ul>
              </div>

              <div class="green-box">
                <div class="list-title">Öğrenme Hedefleri</div>
                  <ul>${goals}</ul>
              </div>
            </div>

            <div class="gray-box">
              <div class="list-title">Uygulama Adımları</div>
              <ol>${instructions}</ol>
            </div>

            ${
              activity.learningOutcomesSummary
                ? `
                  <div class="gray-box">
                    <div class="list-title">Öğrenme Çıktısı Özeti</div>
                    <div class="summary-box">${escapeHtml(activity.learningOutcomesSummary)}</div>
                  </div>
                `
                : ''
            }

            ${
              assessmentQuestions
                ? `
                  <div class="assessment-box">
                    <div class="list-title">Değerlendirme Soruları</div>
                    <ul>${assessmentQuestions}</ul>
                  </div>
                `
                : ''
            }

            ${
              activity.differentiationNotes
                ? `
                  <div class="gray-box">
                    <div class="list-title">Farklılaştırma</div>
                    <div class="summary-box">${escapeHtml(activity.differentiationNotes)}</div>
                  </div>
                `
                : ''
            }

            ${
              activity.familyCommunityNotes
                ? `
                  <div class="gray-box">
                    <div class="list-title">Aile / Toplum Katılımı</div>
                    <div class="summary-box">${escapeHtml(activity.familyCommunityNotes)}</div>
                  </div>
                `
                : ''
            }
          </div>
        `;
      })
      .join('');

    const aiSectionHtml = aiExplanation
      ? `
        <div class="section-card">
          <h2 class="section-title">YZ Destekli Plan Özeti</h2>
          <p class="muted"><strong>Kaynak:</strong> ${escapeHtml(aiExplanation.source)}</p>
          <div class="summary-box">${escapeHtml(aiExplanation.summary)}</div>
        </div>  
      `
      : '';

    const html = `
      <html lang="tr">
        <head>
          <meta charset="UTF-8" />
          <title>Etkinlik Raporu</title>
          <style>${printStyles}</style>
        </head>

        <body>
          <div class="report-root">

            <div class="cover-page">
              <div class="cover-title">ETKİNLİK PLANI RAPORU</div>

              <div class="cover-subtitle">
                ${escapeHtml(classProfile.className)}
              </div>

              <div class="cover-subtitle">
                ${escapeHtml(teacherProfile.schoolName || '-')}
              </div>

              <div class="cover-info">
                <strong>Hazırlayan:</strong> ${escapeHtml(teacherProfile.name)}<br />
                <strong>Yaş Grubu:</strong> ${escapeHtml(classProfile.ageGroup)} yıl<br />
                <strong>Sınıf Mevcudu:</strong> ${classProfile.classSize} öğrenci<br />
                <strong>Tarih:</strong> ${new Date().toLocaleDateString('tr-TR')}
              </div>
            </div>

            <div class="page-break"></div>

            <h1 class="report-title">Etkinlik Raporu</h1>
            <p class="report-subtitle">
              Öğretmen ve sınıf bilgilerine göre oluşturulmuş plan
            </p>

            <div class="top-grid">
              <div class="top-column">
                <div class="info-card">
                  <h2 class="section-title">Öğretmen Bilgileri</h2>
                  <div class="meta-list">
                    <div class="meta-label">Ad</div>
                    <div class="meta-value">${escapeHtml(teacherProfile.name)}</div>

                    <div class="meta-label">Okul</div>
                    <div class="meta-value">${escapeHtml(teacherProfile.schoolName || '-')}</div>

                    <div class="meta-label">Deneyim</div>
                    <div class="meta-value">${
                      teacherProfile.yearsExperience === '' ? '-' : teacherProfile.yearsExperience
                    } yıl</div>

                    <div class="meta-label">Öğretim Stili</div>
                    <div class="meta-value">${escapeHtml(
                      translateTeachingStyle(teacherProfile.teachingStyle),
                    )}</div>
                  </div>
                </div>
              </div>

              <div class="top-column">
                <div class="info-card">
                  <h2 class="section-title">Sınıf Bilgileri</h2>
                  <div class="meta-list">
                    <div class="meta-label">Sınıf</div>
                    <div class="meta-value">${escapeHtml(classProfile.className)}</div>

                    <div class="meta-label">Yaş Grubu</div>
                    <div class="meta-value">${escapeHtml(classProfile.ageGroup)} yıl</div>

                    <div class="meta-label">Sınıf Mevcudu</div>
                    <div class="meta-value">${classProfile.classSize} öğrenci</div>

                    <div class="meta-label">Tahmini Süre</div>
                    <div class="meta-value">${totalDuration} dakika</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="section-card">
              <h2 class="section-title">Plan Özeti</h2>
              <p class="muted">
                Bu rapor toplam ${activities.length} etkinlikten oluşmaktadır.
                Tahmini uygulama süresi ${totalDuration} dakikadır.
              </p>

              <div class="summary-grid">
                <div class="summary-item">
                  <div class="summary-label">Toplam Etkinlik</div>
                  <div class="summary-value">${activities.length}</div>
                </div>

                <div class="summary-item">
                  <div class="summary-label">Toplam Süre</div>
                  <div class="summary-value">${totalDuration} dk</div>
                </div>

                <div class="summary-item">
                  <div class="summary-label">Yaş Grubu</div>
                  <div class="summary-value">${escapeHtml(classProfile.ageGroup)}</div>
                </div>
              </div>

              <div class="badges">
                ${activities
                  .map(
                    (activity) =>
                      `<span class="badge">${escapeHtml(translateSubject(activity.subject))}</span>`,
                  )
                  .join('')}
              </div>
            </div>

            ${aiSectionHtml}

            ${activitiesHtml}

            <div class="footer">
              Erken Çocukluk Etkinlik Planlama Sistemi
            </div>

          </div>
        </body>
      </html>
    `;

    if (Capacitor.isNativePlatform()) {
      try {
        const pdf = await PdfGenerator.fromData({
          data: html,
          documentSize: 'A4',
          orientation: 'portrait',
          type: 'base64',
          fileName: 'etkinlik-raporu.pdf',
        });

        const base64Data = 
          (pdf as any).base64 ||
          (pdf as any).base64Data ||
          (pdf as any).data;

        if (!base64Data) {
          throw new Error('PDF verisi alınamadı.');
        }
        const filename = `etkinlik-raporu-${Date.now()}.pdf`;

        const savedFile = await Filesystem.writeFile({
          path: filename,
          data: base64Data,
          directory: Directory.Documents,
          recursive: true,
        });

        toast.success('PDF oluşturuldu. Paylaşım ekranı açılıyor...');

        await Share.share({
            title: 'Etkinlik Raporu',
            text: 'Etkinlik planı raporu',
            url: savedFile.uri,
            dialogTitle: 'PDF Raporu Paylaş',
          });

          return;
        } catch (error) {
          console.error('PDF paylaşım hata:', error);
          toast.error('PDF paylaşımı başarısız. Lütfen tekrar deneyin.');
          return;
        }
      }

    const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);  
    const printWindow = window.open(url, '_blank', 'width=1200,height=900');

    if (!printWindow) {
      URL.revokeObjectURL(url);
      toast.error('Yazdırma penceresi açılamadı.');
      return;
    }

    printWindow.onload = () => {
      setTimeout(() => {
        printWindow.focus();
        printWindow.print();
        printWindow.close();
        URL.revokeObjectURL(url);
      }, 300);
    };
  };

  const translateSubject = (subject: string) => {
    const map: Record<string, string> = {
      Math: 'Matematik',
      Language: 'Dil Gelişimi',
      Art: 'Sanat',
      Science: 'Fen ve Doğa',
      Music: 'Müzik',
      Physical: 'Fiziksel Gelişim',
      'Social-Emotional': 'Sosyal-Duygusal Gelişim',
    };
    return map[subject] || subject;
  };

  const translateGroupSize = (groupSize: string) => {
    const map: Record<string, string> = {
      Individual: 'Bireysel',
      'Small Group': 'Küçük Grup',
      'Whole Class': 'Tüm Sınıf',
    };
    return map[groupSize] || groupSize;
  };

  const normalizeTeachingStyle = (style: string) => {
    const map: Record<string, string> = {
      structured: 'structured',
      Structured: 'structured',
      balanced: 'balanced',
      Balanced: 'balanced',
      exploratory: 'exploratory',
      Exploratory: 'exploratory',
      'Play-based': 'play_based',
      'play-based': 'play_based',
      'Child-led': 'child_led',
      'child-led': 'child_led',
      Interactive: 'interactive',
      interactive: 'interactive',
      Creative: 'creative',
      creative: 'creative',
    };

    return map[style] || style;
  };

  const translateTeachingStyle = (style: string) => {
    const normalized = normalizeTeachingStyle(style);

    const map: Record<string, string> = {
      structured: 'Yapılandırılmış',
      balanced: 'Dengeli',
      exploratory: 'Keşfetmeye Dayalı',
      play_based: 'Oyun Temelli',
      child_led: 'Çocuk Merkezli',
      interactive: 'Etkileşimli',
      creative: 'Yaratıcı',
    };

    return map[normalized] || style;
  };

  const translateDuration = (duration: string) => {
    const map: Record<string, string> = {
      '5-15min': '5-15 dakika',
      '15-30min': '15-30 dakika',
      '30-45min': '30-45 dakika',
      '45-60min': '45-60 dakika',
    };
    return map[duration] || duration;
  };

  const totalDuration = activities.reduce((acc, activity) => {
    const durationMap: Record<string, number> = {
      '5-15min': 15,
      '15-30min': 30,
      '30-45min': 45,
      '45-60min': 60,
    };
    return acc + (durationMap[activity.duration] || 0);
  }, 0);

  if (!open) return null;

  

  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
      <div className="bg-white w-full max-w-4xl max-h-[90vh] rounded-lg shadow-xl overflow-hidden">
        <div className="border-b bg-gray-50 px-6 py-5">
          <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
            <div>
              <p className="text-xs font-medium uppercase tracking-[0.2em] text-gray-500">
                Öğretmen Destek Sistemi
              </p>
              <h2 className="mt-1 text-2xl font-bold text-gray-900">Etkinlik Planı Raporu</h2>
              <p className="mt-2 max-w-2xl text-sm text-gray-600">
                Seçilen etkinlikler, öğretmen ve sınıf profiline göre düzenlenmiş plan özeti.
              </p>
            </div>

            <div className="flex gap-2 self-start">
              <Button onClick={handlePrint}>
                <Printer className="h-4 w-4 mr-2" />
                {Capacitor.isNativePlatform() ? 'PDF Kaydet / Paylaş' : 'Yazdır'}
              </Button>
              <Button variant="outline" onClick={onClose}>
                Kapat
              </Button>
            </div>
          </div>
        </div>

        <div className="max-h-[calc(90vh-96px)] overflow-y-auto px-6 py-5 bg-gray-100/40 report-section">
          <div className="space-y-6" id="report-content">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="rounded-2xl border bg-white p-5 shadow-sm">
                <h3 className="text-base font-semibold text-gray-900 mb-3">Öğretmen Bilgileri</h3>
                <div className="grid grid-cols-1 gap-2 text-sm">
                  <div className="grid grid-cols-[140px_1fr] gap-3 border-b pb-2 items-start report-row">
                    <span className="text-gray-500">Ad</span>
                    <span className="font-medium text-gray-900">{teacherProfile.name || '-'}</span>
                  </div>
                  <div className="grid grid-cols-[140px_1fr] gap-3 border-b pb-2 items-start report-row">
                    <span className="text-gray-500">Okul</span>
                    <span className="font-medium text-gray-900">{teacherProfile.schoolName || '-'}</span>
                  </div>
                  <div className="grid grid-cols-[140px_1fr] gap-3 border-b pb-2 items-start report-row">
                    <span className="text-gray-500">Deneyim</span>
                    <span className="font-medium text-gray-900">{teacherProfile.yearsExperience === '' ? '-' : teacherProfile.yearsExperience} yıl</span>
                  </div>
                  <div className="grid grid-cols-[140px_1fr] gap-3 border-b pb-2 items-start report-row">
                    <span className="text-gray-500">Öğretim Stili</span>
                    <span className="font-medium text-gray-900">
                      {translateTeachingStyle(teacherProfile.teachingStyle || '')}
                    </span>
                  </div>
                </div>
              </div>

              <div className="rounded-2xl border bg-white p-5 shadow-sm report-section">
                <h3 className="text-base font-semibold text-gray-900 mb-3">Sınıf Bilgileri</h3>
                <div className="grid grid-cols-1 gap-2 text-sm">
                  <div className="grid grid-cols-[140px_1fr] gap-3 border-b pb-2 items-start report-row">
                    <span className="text-gray-500">Sınıf</span>
                    <span className="font-medium text-gray-900">{classProfile.className || '-'}</span>
                  </div>
                  <div className="grid grid-cols-[140px_1fr] gap-3 border-b pb-2 items-start report-row">
                    <span className="text-gray-500">Yaş Grubu</span>
                    <span className="font-medium text-gray-900">{classProfile.ageGroup || '-'} yıl</span>
                  </div>
                  <div className="grid grid-cols-[140px_1fr] gap-3 border-b pb-2 items-start report-row">
                    <span className="text-gray-500">Sınıf Mevcudu</span>
                    <span className="font-medium text-gray-900">{classProfile.classSize ?? '-'} öğrenci</span>
                  </div>
                  <div className="grid grid-cols-[140px_1fr] gap-3 border-b pb-2 items-start report-row">
                    <span className="text-gray-500">Toplam Etkinlik</span>
                    <span className="font-medium text-gray-900">{activities.length}</span>
                  </div>
                  <div className="grid grid-cols-[140px_1fr] gap-3 border-b pb-2 items-start report-row">
                    <span className="text-gray-500">Tahmini Süre</span>
                    <span className="font-medium text-gray-900">{totalDuration ?? '-'} dakika</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="rounded-2xl border bg-white p-5 shadow-sm report-section">
              <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <div>
                  <h3 className="text-base font-semibold text-gray-900">Plan Özeti</h3>
                  <p className="text-sm text-gray-500 mt-1">
                    Seçilen etkinliklerin alanlara göre dağılımı
                  </p>
                </div>
                <div className="text-sm text-gray-600">
                  Toplam <span className="font-semibold text-gray-900">{activities.length}</span> etkinlik
                </div>
              </div>

              <div className="mt-4 flex flex-wrap gap-2">
                {Array.from(new Set(activities.map((a) => a.subject))).map((subject) => (
                  <Badge key={subject} className={`${getSubjectColor(subject)} badge-export px-3 py-1`}>
                    {translateSubject(subject)} ({activities.filter((a) => a.subject === subject).length})
                  </Badge>
                ))}
              </div>
              <div className="mt-4 grid grid-cols-3 gap-4">
                <div className="rounded-lg border p-3 bg-blue-50">
                  <p className="text-sm text-gray-500">Toplam Etkinlik</p>
                  <p className="text-2xl font-bold">{activities.length}</p>
                </div>

                <div className="rounded-lg border p-3 bg-green-50">
                  <p className="text-sm text-gray-500">Toplam Süre</p>
                  <p className="text-2xl font-bold">{totalDuration} dk</p>
                </div>

                <div className="rounded-lg border p-3 bg-purple-50">
                  <p className="text-sm text-gray-500">Yaş Grubu</p>
                  <p className="text-2xl font-bold">{classProfile.ageGroup}</p>
                </div>
              </div>
            </div>
            
            {aiExplanation && (
              <div className="mt-6 rounded-lg border p-4 report-section">
                <h3 className="font-semibold text-lg">YZ Destekli Plan Özeti</h3>

                <p className="mt-2 text-sm text-muted-foreground">
                  Kaynak: {aiExplanation.source}
                </p>

                <p className="mt-3">{aiExplanation.summary}</p>

                <div className="mt-4 space-y-3">
                  {aiExplanation.activity_explanations.map((item) => (
                    <div key={item.activity_id} className="rounded-lg border p-3">
                      <h4 className="font-semibold">{item.title}</h4>

                      <p className="mt-2 text-sm">{item.explanation}</p>

                      <p className="mt-2 text-sm">
                        <strong>Öğretmen rehberi:</strong> {item.teacher_guidance}
                      </p>

                      <p className="mt-2 text-sm">
                        <strong>Farklılaştırma önerisi:</strong> {item.adaptation}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="space-y-4">
              <h3 className="text-xl font-semibold">📚 Planlanan Etkinlikler</h3>
              <p className="text-sm text-gray-500">
                Bu plan toplam {activities.length} etkinlik ve
                yaklaşık {totalDuration} dakika sürmektedir.
              </p>
              {activities.map((activity, index) => (
                <div key={activity.id} className="activity-card rounded-2xl border bg-white p-5 shadow-sm">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <h4 className="text-lg font-bold bg-indigo-50 border-1-4 border-indigo-600 p-3 rounded-lg">
                        {index + 1}. {activity.title}
                      </h4>
                      <div className="flex flex-wrap gap-2 mt-2">
                        <Badge className={`${getSubjectColor(activity.subject)} badge-export`}>
                          {translateSubject(activity.subject)}
                        </Badge>
                        <Badge variant="outline" className="flex items-center gap-1 badge-export">
                          <Clock className="h-3 w-3" />
                          {translateDuration(activity.duration)}
                        </Badge>
                        <Badge variant="outline" className="flex items-center gap-1 badge-export">
                          <Users className="h-3 w-3" />
                          {translateGroupSize(activity.groupSize)}
                        </Badge>
                      </div>
                    </div>
                  </div>

                  <p className="text-sm leading-6 text-gray-600 mb-4">{activity.description}</p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm report-section">
                    <div className="rounded-xl border-l-4 border-blue-500 bg-blue-50 p-4">
                      <p className="font-semibold mb-2 text-gray-900">Materyaller</p>
                      <ul className="list-disc list-inside text-gray-700 space-y-1 leading-6">
                        {activity.materials.map((material, i) => (
                          <li key={i}>{material}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="rounded-xl border-l-4 border-green-500 bg-green-50 p-4">
                      <p className="font-semibold mb-2 text-gray-900">Öğrenme Hedefleri</p>
                      <ul className="list-disc list-inside text-gray-700 space-y-1 leading-6">
                        {activity.learningGoals.map((goal, i) => (
                          <li key={i}>{goal}</li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  <div className="mt-3 report-section">
                    <p className="font-semibold mb-1 text-sm">Uygulama Adımları:</p>
                    <ol className="list-decimal list-inside text-gray-600 space-y-1 text-sm">
                      {activity.instructions.map((instruction, i) => (
                        <li key={i}>{instruction}</li>
                      ))}
                    </ol>
                  </div>

                  {activity.learningOutcomesSummary && (
                    <div className="mt-4 rounded-xl bg-gray-50 border p-4 report-section">
                      <p className="font-semibold mb-2 text-sm text-gray-900">Öğrenme Çıktısı Özeti</p>
                      <p className="text-sm leading-6 text-gray-700">{activity.learningOutcomesSummary}</p>
                    </div>
                  )}

                  {activity.assessmentQuestions && activity.assessmentQuestions.length > 0 && (
                    <div className="mt-4 rounded-xl border border-emerald-300 bg-emerald-50 p-4 report-section">
                      <p className="font-semibold mb-2 text-sm text-gray-900">Değerlendirme Soruları</p>
                      <ul className="list-disc list-inside text-gray-700 space-y-1 text-sm leading-6">
                        {activity.assessmentQuestions.map((question, i) => (
                          <li key={i}>{question}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {activity.differentiationNotes && (
                    <div className="mt-4 rounded-xl bg-gray-50 border p-4 report-section">
                      <p className="font-semibold mb-2 text-sm text-gray-900">Farklılaştırma</p>
                      <p className="text-sm leading-6 text-gray-700">{activity.differentiationNotes}</p>
                    </div>
                  )}

                  {activity.familyCommunityNotes && (
                    <div className="mt-4 rounded-xl bg-gray-50 border p-4 report-section">
                      <p className="font-semibold mb-2 text-sm text-gray-900">Aile / Toplum Katılımı</p>
                      <p className="text-sm leading-6 text-gray-700">{activity.familyCommunityNotes}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

}  
