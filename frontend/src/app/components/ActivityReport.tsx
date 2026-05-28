import { Activity } from '../types/activity';
import { TeacherProfile, ClassProfile } from '../types/profile';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { ScrollArea } from './ui/scroll-area';
import { Printer, Clock, Users } from 'lucide-react';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { Filesystem, Directory } from '@capacitor/filesystem';
import { Capacitor } from '@capacitor/core';
import { toast } from 'sonner';

async function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onloadend = () => {
      const result = reader.result;

      if (typeof result !== 'string') {
        reject(new Error('Blob verisi base64 formatına dönüştürülemedi.'));
        return;
      }

      const base64 = result.split(',')[1];
      resolve(base64);
    };

    reader.onerror = () => {
      reject(new Error('Blob okunurken hata oluştu.'));
    };

    reader.readAsDataURL(blob);
  });
}

interface ActivityReportProps {
  activities: Activity[];
  teacherProfile: TeacherProfile;
  classProfile: ClassProfile;
  open: boolean;
  onClose?: () => void;
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
  const handlePrint = async () => {
    const element = document.getElementById('report-content');
    
    if (!element) {
      toast.error('Rapor içeriği bulunamadı');
      return;
    }

    if (!Capacitor.isNativePlatform()) {
      const html = `
        <!DOCTYPE html>
        <html lang="tr">
          <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Etkinlik Raporu</title>
            <style>
              body {
                font-family: Arial, sans-serif;
                padding: 24px;
                color: #111827;
                background: #ffffff;
              }

              h1, h2, h3, h4 {
                margin-top: 0;
              }

              .activity-card {
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 16px;
                page-break-inside: avoid;
                break-inside: avoid;
              }

              .badge-export {
                display: inline-block;
                border: 1px solid #d1d5db;
                border-radius: 9999px;
                padding: 4px 10px;
                margin-right: 6px;
                margin-bottom: 6px;
                background: #f3f4f6;
                color: #111827;
                font-size: 12px;
              }

              .text-gray-500,
              .text-gray-600,
              .text-muted-foreground {
                color: #4b5563 !important;
              }

              ul, ol {
                padding-left: 20px;
              }

              @page {
                margin: 18mm;
              }
            </style>
          </head>
          <body>
            ${element.innerHTML}
          </body>
        </html>
      `;

      const blob = new Blob([html], { type: 'text/html' });
      const url = URL.createObjectURL(blob);

      const printWindow = window.open(url, '_blank', 'width=1000,height=1400');

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
        }, 500);
      };

      return;
    }   

    try {
      const canvas = await html2canvas(element, { 
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff',
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');

      const pageWidth = 210; // A4 sayfa genişliği mm cinsinden
      const pageHeight = 297; // A4 sayfa yüksekliği mm cinsinden
      const margin = 10; // Kenar boşluğu mm cinsinden
      const usableWidth = pageWidth - margin * 2;
      const usableHeight = pageHeight - margin * 2;
      
      const imgWidth = usableWidth;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      let heightLeft = imgHeight;
      let position = margin;

      pdf.addImage(imgData, 'PNG', margin, position, imgWidth, imgHeight);
      heightLeft -= usableHeight;

      while (heightLeft > 0) {
        position = heightLeft - imgHeight + margin;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', margin, position, imgWidth, imgHeight);
        heightLeft -= usableHeight;
      }

      const pdfBlob = pdf.output('blob');
      const fileName = 'etkinlik-raporu.pdf';

      if (Capacitor.isNativePlatform()) {
        const base64Data = await blobToBase64(pdfBlob);
        const filePath = `documents/${fileName}`;
          
       await Filesystem.writeFile({
        path: filePath,
        data: base64Data,
        directory: Directory.Documents,
        recursive: true,
      });

      toast.success('PDF başarıyla oluşturuldu.');
    }
  } catch (error) {
      console.error('PDF oluşturma hatası:', error);
      toast.error('PDF oluşturulamadı.');
  }
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

  const translateTeachingStyle = (style: string) => {
    const map: Record<string, string> = {
      balanced: 'Dengeli',
      'Play-based': 'Oyun Temelli',
      Structured: 'Yapılandırılmış',
      'Child-led': 'Çocuk Merkezli',
    };
    return map[style] || style;
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

  const totalDuration = activities.reduce((acc, activity) => {
    const duration = activity.duration.split('-')[1].replace('min', '');
    return acc + parseInt(duration);
  }, 0);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
      <div className="bg-white w-full max-w-4xl max-h-[90vh] rounded-lg shadow-xl overflow-hidden">
        <div className="flex items-center justify-between p-4 border-b">
          <div>
            <h2 className="text-xl font-semibold">Etkinlik Planı Raporu</h2>
            <p className="text-sm text-gray-500">
              Oluşturduğun etkinlik planını inceleyebilir ve çıktısını alabilirsin
            </p>
          </div>

          <div className="flex gap-2">
            <Button onClick={handlePrint}>
              <Printer className="h-4 w-4 mr-2" />
              {Capacitor.isNativePlatform() ? 'PDF Dışa Aktar' : 'Yazdır'}
            </Button>
            <Button variant="outline" onClick={onClose}>
              Kapat
            </Button>
          </div>
        </div>

        <ScrollArea className="max-h-[calc(90vh-80px)] p-4">
          <div className="space-y-6" id="report-content">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="border rounded-lg p-4">
                <h3 className="font-semibold mb-2">Öğretmen Bilgileri</h3>
                <div className="space-y-1 text-sm">
                  <p><strong>Ad:</strong> {teacherProfile.name}</p>
                  <p><strong>Okul:</strong> {teacherProfile.schoolName}</p>
                  <p><strong>Deneyim:</strong> {teacherProfile.yearsExperience} yıl</p>
                  <p><strong>Öğretim Stili:</strong> {translateTeachingStyle(teacherProfile.teachingStyle)}</p>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h3 className="font-semibold mb-2">Sınıf Bilgileri</h3>
                <div className="space-y-1 text-sm">
                  <p><strong>Sınıf:</strong> {classProfile.className}</p>
                  <p><strong>Yaş Grubu:</strong> {classProfile.ageGroup} yıl</p>
                  <p><strong>Sınıf Mevcudu:</strong> {classProfile.classSize} öğrenci</p>
                  <p><strong>Toplam Etkinlik:</strong> {activities.length}</p>
                  <p><strong>Tahmini Süre:</strong> {totalDuration} dakika</p>
                </div>
              </div>
            </div>

            <div className="border rounded-lg p-4">
              <h3 className="font-semibold mb-2">Plan Özeti</h3>
              <div className="flex flex-wrap gap-2">
                {Array.from(new Set(activities.map((a) => a.subject))).map((subject) => (
                  <Badge key={subject} className={`${getSubjectColor(subject)} badge-export`}>
                    {translateSubject(subject)} ({activities.filter((a) => a.subject === subject).length})
                  </Badge>
                ))}
              </div>
            </div>
            
            {aiExplanation && (
              <div className="mt-6 rounded-lg border p-4">
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
              <h3 className="font-semibold">Planlanan Etkinlikler</h3>
              {activities.map((activity, index) => (
                <div key={activity.id} className="activity-card border rounded-lg p-4">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <h4 className="font-semibold">
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

                  <p className="text-sm text-gray-600 mb-3">{activity.description}</p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="font-semibold mb-1">Materyaller:</p>
                      <ul className="list-disc list-inside text-gray-600 space-y-1">
                        {activity.materials.map((material, i) => (
                          <li key={i}>{material}</li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <p className="font-semibold mb-1">Öğrenme Hedefleri:</p>
                      <ul className="list-disc list-inside text-gray-600 space-y-1">
                        {activity.learningGoals.map((goal, i) => (
                          <li key={i}>{goal}</li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  <div className="mt-3">
                    <p className="font-semibold mb-1 text-sm">Uygulama Adımları:</p>
                    <ol className="list-decimal list-inside text-gray-600 space-y-1 text-sm">
                      {activity.instructions.map((instruction, i) => (
                        <li key={i}>{instruction}</li>
                      ))}
                    </ol>
                  </div>

                  {activity.learningOutcomesSummary && (
                    <div className="mt-3">
                      <p className="font-semibold mb-1 text-sm">Öğrenme Çıktısı Özeti:</p>
                      <p className="text-sm text-gray-600">{activity.learningOutcomesSummary}</p>
                    </div>
                  )}

                  {activity.assessmentQuestions && activity.assessmentQuestions.length > 0 && (
                    <div className="mt-3">
                      <p className="font-semibold mb-1 text-sm">Değerlendirme Soruları:</p>
                      <ul className="list-disc list-inside text-gray-600 space-y-1 text-sm">
                        {activity.assessmentQuestions.map((question, i) => (
                          <li key={i}>{question}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {activity.differentiationNotes && (
                    <div className="mt-3">
                      <p className="font-semibold mb-1 text-sm">Farklılaştırma:</p>
                      <p className="text-sm text-gray-600">{activity.differentiationNotes}</p>
                    </div>
                  )}

                  {activity.familyCommunityNotes && (
                    <div className="mt-3">
                      <p className="font-semibold mb-1 text-sm">Aile / Toplum Katılımı:</p>
                      <p className="text-sm text-gray-600">{activity.familyCommunityNotes}</p>
                    </div>
                  )}

                </div>
              ))}
            </div>
          </div>
        </ScrollArea>
      </div>

      <style>{`
        .pdf-export-mode,
        .pdf-export-mode * {
          color: #111827 !important;
          border-color: #d1d5db !important;
          box-shadow: none !important;
          text-shadow: none !important;
        }

        .pdf-export-mode {
          background: #ffffff !important;
        }

        .pdf-export-mode .border,
        .pdf-export-mode [class*="border"] {
          border-color: #d1d5db !important;
        }

        .pdf-export-mode .bg-white,
        .pdf-export-mode [class*="bg-"] {
          background: #ffffff !important;
        }

        .pdf-export-mode .text-gray-500,
        .pdf-export-mode .text-gray-600,
        .pdf-export-mode .text-muted-foreground {
          color: #4b5563 !important;
        }

        .pdf-export-mode .badge-export {
          background: #e5e7eb !important;
          color: #111827 !important;
          border: 1px solid #d1d5db !important;
        }
      `}</style>
    </div>
  );
}